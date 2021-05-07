# Extract data in clean tall parquet for temperature model

import datetime as dt
import logging

import pandas as pd
import utils
from dask import dataframe as dd
from sklearn.impute import KNNImputer

###################
# Logging
###################

logger = logging.getLogger(__name__)
utils.setup_logging()


###################
# Functions
###################


def extract_t_data(from_year: int, s3_bucket: str) -> pd.DataFrame:
    columns_to_extract = ["numer_sta", "date", "t"]
    filters = [[("YEAR", ">=", from_year)]]
    df = dd.read_parquet(
        f"{s3_bucket}Raw/METEOFRANCE/synop/",
        columns=columns_to_extract,
        filters=filters,
        index=False,
    ).compute()
    return df


def pivot_t_data(synop_df: pd.DataFrame) -> pd.DataFrame:
    meteo_format = "%Y%m%d%H%M%S"
    df = synop_df.copy()

    # Set datetime index
    df["delivery_from"] = pd.to_datetime(df.date, format=meteo_format, utc=True)
    df = df.rename(columns={"numer_sta": "station_id"}).drop_duplicates()

    return df.pivot(columns="station_id", values="t", index="delivery_from")


def fill_missing_values(pivot_df: pd.DataFrame) -> pd.DataFrame:
    # Looking at the 4 closest stations in distance (t wise) to fill gaps
    imputer = KNNImputer(n_neighbors=4, weights="distance")

    return pd.DataFrame(
        imputer.fit_transform(pivot_df.transpose().to_numpy()).transpose(),
        columns=pivot_df.columns,
        index=pivot_df.index,
    )


def interpolate_to_hh(df: pd.DataFrame) -> pd.DataFrame:
    # Linear interpolation as performed by enedis
    index = pd.date_range(start=df.index.min(), end=df.index.max(), freq="30T")
    return df.reindex(index).interpolate(method="linear", axis=0)


def create_output_path(run_date: dt.date, s3_bucket: str) -> str:
    now = dt.datetime.now()
    return (
        f"{s3_bucket}Staging/Extracts/type=WEATHER/asset=T2M/"
        f"category=SYNOP/settlement_run=HISTORICAL/"
        f"valid_at={run_date.isoformat()}/{now.isoformat()}.parquet"
    )


def etl_synop(run_date: dt.date, from_year: int, s3_bucket: str):
    df = extract_t_data(from_year=from_year, s3_bucket=s3_bucket)
    df = pivot_t_data(df)
    df = fill_missing_values(df)
    df = interpolate_to_hh(df)

    hive_partitions = {
        "type": "WEATHER",
        "asset": "T2M",
        "category": "SYNOP",
        "settlement_run": "ACT",
        "created_at": f"{run_date:%Y-%m-%dT%H:%M:%S}",
    }
    utils.hive_parquet_save(
        df=df.reset_index(),
        s3_bucket=f"{s3_bucket}Staging/Extracts/",
        hive_partitions=hive_partitions,
    )

    logger.info(f"mf synop for {run_date:%Y-%m-%d} saved in {s3_bucket}")


###################
# Commands
###################

__all__ = [
    "etl_synop",
]
TODAY = dt.date.today()
S3_BUCKET = "s3://noos-prod-neptune-services/"

if __name__ == "__main__":
    etl_synop(run_date=TODAY, from_year=2016, s3_bucket=S3_BUCKET)
