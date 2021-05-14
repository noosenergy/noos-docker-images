import datetime as dt
import logging
from typing import List, Tuple

import pandas as pd
import utils
from dateutil.relativedelta import relativedelta

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
    "profile_class": "str",
    "delivery_from": "datetime64[ns, UTC]",
    "coefficient_value": "float32",
}


def extract_profile_data(
    dataset: str,
    s3_bucket: str,
    filters: List[List[Tuple[str, str, str]]] = None,
) -> pd.DataFrame:
    if dataset == "coefficients-des-profils":
        value = "coefficient_dynamique"
    elif dataset == "coefficients-de-profils-dynamiques-anticipes-en-j1":
        value = "coefficient_dynamique_j_1"
    else:
        raise NotImplementedError(f"dataset {dataset} not implemented")

    base_columns = ["horodate", "sous_profil"]
    df = pd.read_parquet(
        f"{s3_bucket}Raw/ENEDIS/{dataset}/",
        columns=base_columns + [value],
        filters=filters,
    )

    # Set datetime index
    iso_format = "%Y-%m-%dT%H:%M:%S%z"
    df["delivery_from"] = pd.to_datetime(df.horodate, format=iso_format, utc=True)
    df = df.rename(
        columns={"sous_profil": "profile_class", value: "coefficient_value"}
    ).drop_duplicates()

    return df


def save_profile_data_act_tall(
    run_date: dt.date,
    s3_bucket: str,
):

    tall_act_df = extract_profile_data(
        dataset="coefficients-des-profils",
        s3_bucket=s3_bucket,
        filters=[
            [("year", ">=", f"{run_date:%Y}")],
        ],
    )

    hive_partitions = {
        "asset": "PWRTE",
        "category": "DYNAMIC",
        "settlement_run": "ACT",
        "created_at": f"{run_date:%Y-%m-%dT00:00:00}",
    }
    utils.datalake_wrangler_save(
        df=tall_act_df.drop_duplicates(),
        s3_bucket=f"{s3_bucket}Store/Datalakes/PROFILE_COEFFICIENT/",
        hive_partitions=hive_partitions,
        df_columns_type=COLUMNS_TYPE,
        mode="overwrite_partitions",
    )

    logger.info(
        f"tall enedis ACT profiles for {run_date:%Y} "
        f"saved in {s3_bucket}Store/Datalakes/PROFILE_COEFFICIENT/"
    )


def save_profile_data_prov_tall(
    run_date: dt.date,
    s3_bucket: str,
):

    tall_prov_df = extract_profile_data(
        dataset="coefficients-de-profils-dynamiques-anticipes-en-j1",
        s3_bucket=s3_bucket,
        filters=[
            [("date", ">=", f"{run_date:%Y-%m-%d}")],
        ],
    )

    hive_partitions = {
        "asset": "PWRTE",
        "category": "DYNAMIC",
        "settlement_run": "PROV_1D",
        "created_at": f"{run_date:%Y-%m-%dT00:00:00}",
    }
    utils.datalake_wrangler_save(
        df=tall_prov_df.drop_duplicates(),
        s3_bucket=f"{s3_bucket}Store/Datalakes/PROFILE_COEFFICIENT/",
        hive_partitions=hive_partitions,
        df_columns_type=COLUMNS_TYPE,
        mode="overwrite_partitions",
    )

    logger.info(
        f"tall enedis PROV_1D profiles for {run_date:%Y} "
        f"saved in {s3_bucket}Store/Datalakes/PROFILE_COEFFICIENT/"
    )


def save_profile_data_full_pivot(
    run_date: dt.date,
    s3_bucket: str,
):

    act_df = extract_profile_data(
        dataset="coefficients-des-profils",
        s3_bucket=s3_bucket,
        filters=[
            [("year", ">=", "2018"), ("month", ">=", "7")],
            [("year", ">=", "2019")],
        ],
    )

    last_2_weeks = run_date - relativedelta(weeks=2)
    prov_df = extract_profile_data(
        dataset="coefficients-de-profils-dynamiques-anticipes-en-j1",
        s3_bucket=s3_bucket,
        filters=[[("date", ">=", last_2_weeks.isoformat())]],
    )

    df = pd.concat([act_df, prov_df], ignore_index=True).drop_duplicates(
        ["profile_class", "delivery_from"]
    )
    pivot_df = df.pivot(
        index="delivery_from", columns="profile_class", values="coefficient_value"
    )

    hive_partitions = {
        "asset": "PWRTE",
        "category": "DYNAMIC",
        "created_at": run_date.isoformat(),
    }
    utils.datalake_wrangler_save(
        df=pivot_df,
        s3_bucket=f"{s3_bucket}Staging/Extracts/PROFILE_COEFFICIENT/",
        hive_partitions=hive_partitions,
        mode="overwrite_partitions",
    )

    logger.info(
        f"full pivot enedis profiles for {run_date:%Y-%m-%d} "
        f"saved in {s3_bucket}Staging/Extracts/PROFILE_COEFFICIENT/"
    )


###################
# Commands
###################

TODAY = dt.date.today()
YESTERDAY = TODAY - relativedelta(days=1)
LAST_2_WEEKS = TODAY - relativedelta(weeks=2)
S3_BUCKET = "s3://noos-prod-neptune-services/"

if __name__ == "__main__":

    if LAST_2_WEEKS.year != TODAY.year:
        save_profile_data_act_tall(
            run_date=LAST_2_WEEKS,
            s3_bucket=S3_BUCKET,
        )

    save_profile_data_act_tall(
        run_date=TODAY,
        s3_bucket=S3_BUCKET,
    )

    # save PROV data fro yesterday
    save_profile_data_prov_tall(
        run_date=YESTERDAY,
        s3_bucket=S3_BUCKET,
    )

    # Save full data as pivot in Staging for quick access
    save_profile_data_full_pivot(
        run_date=TODAY,
        s3_bucket=S3_BUCKET,
    )
