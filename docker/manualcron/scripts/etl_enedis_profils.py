import datetime as dt
import logging
from typing import List, Tuple

import pandas as pd
import utils
from dask import dataframe as dd
from dateutil import relativedelta

###################
# Logging
###################

logger = logging.getLogger(__name__)
utils.setup_logging()


###################
# Functions
###################


def extract_pivot_profil_data(
    dataset: str,
    value: str,
    s3_bucket: str,
    filters: List[List[Tuple[str, str, str]]] = None,
) -> pd.DataFrame:
    base_columns = ["horodate", "sous_profil"]
    df = dd.read_parquet(
        f"{s3_bucket}Raw/ENEDIS/{dataset}/",
        columns=base_columns + [value],
        filters=filters,
        index=False,
    ).compute()

    # Set datetime index
    iso_format = "%Y-%m-%dT%H:%M:%S%z"
    df["delivery_from"] = pd.to_datetime(df.horodate, format=iso_format, utc=True)

    df = df.rename(columns={"sous_profil": "profile_class"}).drop_duplicates()

    return df.pivot(index="delivery_from", columns="profile_class", values=value)


def save_enedis_profils(
    run_date: dt.date,
    dataset: str,
    value: str,
    settlement_run: str,
    s3_bucket: str,
    filters: List[List[Tuple[str, str, str]]] = None,
):
    df = extract_pivot_profil_data(dataset, value, s3_bucket, filters)

    hive_partitions = {
        "type": "PROFILE_COEFFICIENT",
        "asset": "PWRTE",
        "category": "DYNAMIQUE",
        "settlement_run": settlement_run,
        "created_at": f"{run_date:%Y-%m-%dT%H:%M:%S}",
    }
    utils.hive_parquet_save(
        df=df.reset_index(),
        s3_bucket=f"{s3_bucket}Staging/Extracts/",
        hive_partitions=hive_partitions,
    )

    logger.info(f"{dataset} for {run_date:%Y-%m-%d} saved in {s3_bucket}")


###################
# Commands
###################

__all__ = [
    "save_enedis_profils",
]
TODAY = dt.date.today()
LAST_WEEK = TODAY - relativedelta.relativedelta(days=7)
S3_BUCKET = "s3://noos-prod-neptune-services/"
FILTERS = [[("date", ">=", "2018-06-30")]]

if __name__ == "__main__":

    save_enedis_profils(
        run_date=TODAY,
        dataset="coefficients-des-profils",
        value="coefficient_dynamique",
        settlement_run="ACT",
        filters=[[("date", ">=", "2018-06-30")]],
        s3_bucket=S3_BUCKET,
    )

    save_enedis_profils(
        run_date=TODAY,
        dataset="coefficients-de-profils-dynamiques-anticipes-en-j1",
        value="coefficient_dynamique_j_1",
        settlement_run="PROV",
        filters=[[("date", ">=", LAST_WEEK.isoformat())]],
        s3_bucket=S3_BUCKET,
    )
