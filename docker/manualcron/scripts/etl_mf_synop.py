# Extract data in clean tall parquet for temperature model

import datetime as dt
import logging
from typing import List, Optional, Tuple

import pandas as pd
import utils

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
    "t": "float32",
}


def extract_t_data(
    s3_bucket: str,
    partition_filter: Optional[List[List[Tuple[str, str, str]]]] = None,
) -> pd.DataFrame:
    vars_to_keep = ["t"]

    df = pd.read_parquet(
        path=f"{s3_bucket}Raw/METEOFRANCE/synop/",
        columns=["numer_sta", "date"] + vars_to_keep,
        filters=partition_filter,
    )

    # Clean data from duplicates and NA on vars
    df = df.drop_duplicates()
    df = df[~df[vars_to_keep].isna().all(axis=1)]

    # Set datetime index
    meteo_format = "%Y%m%d%H%M%S"
    df["delivery_from"] = pd.to_datetime(df.date, format=meteo_format, utc=True)

    return df.rename(columns={"numer_sta": "station_id"}).drop_duplicates()


def save_t_data_yearly_tall(
    run_date: dt.date,
    s3_bucket: str,
):
    # filling missing value with minimum 1 year of data
    partition_filter = [[("year", ">=", str(run_date.year - 1))]]
    df = extract_t_data(s3_bucket=s3_bucket, partition_filter=partition_filter)

    # pivot needed to fill and interpolate data
    pivot_df = df.pivot(
        index="delivery_from", columns="station_id", values="t"
    ).sort_index()
    pivot_df = utils.fill_missing_values(pivot_df)
    pivot_df = utils.interpolate_to_freq(pivot_df)

    # saving only 1 day in tall format
    pivot_df = pivot_df.loc[f"{run_date:%Y}"]
    tall_df = pivot_df.reset_index().melt(id_vars="delivery_from", value_name="t")

    hive_partitions = {
        "asset": "T2M",
        "category": "SYNOP",
        "year": f"{run_date:%Y}",
    }
    utils.datalake_wrangler_save(
        df=tall_df,
        s3_bucket=f"{s3_bucket}Store/Datalakes/WEATHER/",
        hive_partitions=hive_partitions,
        df_columns_type=COLUMNS_TYPE,
        mode="overwrite_partitions",
    )

    logger.info(
        f"tall mf synop for {run_date:%Y} saved in {s3_bucket}Store/Datalakes/WEATHER/"
    )


def save_t_data_full_pivot(
    run_date: dt.date,
    s3_bucket: str,
):
    # Taking data from 2018 onwards in Datalake
    partition_filter = [[("year", ">=", "2018")]]
    df = pd.read_parquet(
        f"{s3_bucket}Store/Datalakes/WEATHER/",
        columns=list(COLUMNS_TYPE.keys()),
        filters=partition_filter,
    )
    pivot_df = df.drop_duplicates(["station_id", "delivery_from"]).pivot(
        index="delivery_from", columns="station_id", values="t"
    )

    hive_partitions = {
        "asset": "T2M",
        "category": "SYNOP",
        "created_at": run_date.isoformat(),
    }
    # Saving in Staging
    utils.datalake_wrangler_save(
        df=pivot_df,
        s3_bucket=f"{s3_bucket}Staging/Extracts/WEATHER/",
        hive_partitions=hive_partitions,
        mode="overwrite",
    )

    logger.info(
        f"full pivot mf synop for {run_date:%Y-%m-%d} "
        f"saved in {s3_bucket}Staging/Extracts/"
    )


###################
# Commands
###################

TODAY = dt.date.today()
S3_BUCKET = "s3://noos-prod-neptune-services/"

if __name__ == "__main__":

    # Save daily files in datalake
    save_t_data_yearly_tall(
        run_date=TODAY,
        s3_bucket=S3_BUCKET,
    )

    # Save full data as pivot in Staging for quick access
    save_t_data_full_pivot(
        run_date=TODAY,
        s3_bucket=S3_BUCKET,
    )
