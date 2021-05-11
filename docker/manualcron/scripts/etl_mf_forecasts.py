import datetime as dt
import logging
from typing import List, Optional

import fsspec
import numpy as np
import pandas as pd
import utils
import xarray as xr

###################
# Logging
###################

logger = logging.getLogger(__name__)
utils.setup_logging()


###################
# Functions
###################

# important for a consistent parquet schema in the datalake
COLUMNS_TYPE = {
    "station_id": "str",
    "delivery_from": "datetime64[ns, UTC]",
    "t2m": "float32",
    "t2m_min": "float32",
    "t2m_max": "float32",
}


def get_grib_data(ds, field, lats: pd.Series, lons: pd.Series) -> Optional[np.ndarray]:
    """Find values at (lats, lons) coordinates as vectors."""
    if field not in list(ds.variables):
        logger.exception(
            Exception(
                f"{field} not present in variables {list(ds.variables)} "
                f"for valid_time={ds.valid_time.values}"
            )
        )
        return None

    # Trick to transform floats in int to avoid precision error when indexing
    precision = 3

    grid_lat_resolution = ds[field].GRIB_iDirectionIncrementInDegrees
    grid_lon_resolution = ds[field].GRIB_jDirectionIncrementInDegrees

    # create pandas index for lat and lon
    grid_lat = pd.Index(ds["latitude"].round(precision) * 10 ** precision).astype("int")
    grid_lon = pd.Index(ds["longitude"].round(precision) * 10 ** precision).astype(
        "int"
    )

    # Trick to round down to stay in correct grid point
    data_lats = lats // grid_lat_resolution * grid_lat_resolution
    data_lons = lons // grid_lon_resolution * grid_lon_resolution

    data_lats = (data_lats * 10 ** precision).astype("int")
    data_lons = (data_lons * 10 ** precision).astype("int")

    index_lat = grid_lat.get_indexer(data_lats)
    index_lon = grid_lon.get_indexer(data_lons)

    if (index_lat == -1).any() | (index_lon == -1).any():
        raise LookupError("data point not matching ds grid")

    return ds[field].values[index_lat, index_lon]


def extract_forecasts_from_files(
    files: List[str], field, lats: pd.Series, lons: pd.Series, ids: pd.Series
):
    """Loop on files to extract grib data at (lats, lons) coordinates as vectors."""
    forecast = pd.DataFrame()
    files_local = fsspec.open_local(files)
    for f in files_local:
        ds = xr.open_dataset(f, engine="cfgrib")
        values = get_grib_data(ds, field, lats, lons)
        if values is not None:
            date = ds.valid_time.values
            forecast = forecast.append(pd.Series(data=values, index=ids, name=date))

    return forecast.tz_localize("UTC")


def extract_run_forecast(run_datetime: dt.datetime, s3_bucket: str) -> pd.DataFrame:
    stations = pd.read_parquet(s3_bucket + "Store/Datalakes/WEATHER_STATION/")
    stations = stations[stations.in_scope]

    files_all = fsspec.open_files(
        f"{s3_bucket}Raw/METEOFRANCE/arpege-europe/v2/"
        f"{run_datetime:%Y-%m-%d}/{run_datetime:%H}/TMP/2m/*h.grib2"
    )

    if not files_all:
        raise FileNotFoundError(run_datetime)

    files_forecast = dict()
    files_forecast[""] = [
        f"simplecache::s3://{f.path}"
        for f in files_all
        if not (any(substring in f.path for substring in ["min", "max"]))
    ]
    files_forecast["_min"] = [
        f"simplecache::s3://{f.path}" for f in files_all if "min" in f.path
    ]
    files_forecast["_max"] = [
        f"simplecache::s3://{f.path}" for f in files_all if "max" in f.path
    ]

    output = pd.DataFrame()
    merge_columns = ["delivery_from", "station_id"]
    for suffix, files in files_forecast.items():
        df = extract_forecasts_from_files(
            files, "t2m", stations.latitude, stations.longitude, stations.id
        )

        df_interpolate = utils.interpolate_to_freq(df)

        df_melt = pd.melt(
            df_interpolate.reset_index().rename(columns={"index": "delivery_from"}),
            id_vars="delivery_from",
            value_vars=stations.id.values,
            var_name="station_id",
            value_name=f"t2m{suffix}",
        )

        try:
            output = pd.merge(
                output,
                df_melt,
                left_on=merge_columns,
                right_on=merge_columns,
                how="outer",
            )
        except (KeyError, IndexError):
            output = (
                df_melt
                if not df_melt.empty
                else ValueError("both Dataframes are empty")
            )
    return output


def save_run_forecast(run_datetime: dt.datetime, s3_bucket: str):
    df = extract_run_forecast(run_datetime=run_datetime, s3_bucket=s3_bucket)

    hive_partitions = {
        "asset": "T2M",
        "category": "ARPEGE",
        "created_at": f"{run_datetime:%Y-%m-%dT%H:%M:%S}",
    }
    utils.datalake_wrangler_save(
        df=df,
        s3_bucket=f"{s3_bucket}Store/Datalakes/WEATHER_FORECAST/",
        hive_partitions=hive_partitions,
        df_columns_type=COLUMNS_TYPE,
        mode="overwrite",
    )
    logger.info(
        f"mf forecast for {run_datetime:%Y-%m-%dT%H:%M:%S} saved in {s3_bucket}"
    )


###################
# Commands
###################

S3_BUCKET = "s3://noos-prod-neptune-services/"
run_datetime = utils.rounddown_time(timedelta=dt.timedelta(minutes=12 * 60))

if __name__ == "__main__":
    save_run_forecast(run_datetime=run_datetime, s3_bucket=S3_BUCKET)
