import datetime as dt
import logging

import awswrangler as wr
import utils
import utils_enedis
from dateutil.relativedelta import relativedelta

###################
# Logging
###################


logger = logging.getLogger(__name__)
utils.setup_logging()


###################
# Functions
###################


def save_enedis_main_profiles_act(
    dataset: str, data_date: dt.date, s3_bucket: str
) -> None:
    """Save downloaded data in datalake as parquet."""
    dynamic_profiles = [
        "RES1_BASE",
        "RES11_BASE",
        "RES2_HC",
        "RES2_HP",
        "PRO1_BASE",
        "PRO2_HC",
        "PRO2_HP",
    ]

    params = dict()
    params__profils = {"where": " OR ".join(f'"{w}"' for w in dynamic_profiles)}
    params.update(params__profils)

    # Download full month
    params__date = {"refine": f"horodate:{data_date:%Y-%m}"}
    params.update(params__date)
    df = utils_enedis.download_enedis_data(dataset, params)

    if not df.empty:
        wr.s3.to_parquet(
            df=df.drop_duplicates(),
            path=f"{s3_bucket}Raw/ENEDIS/{dataset}/year={data_date:%Y}/month={data_date:%m}/",
            dataset=True,
            index=False,
            compression="snappy",
            mode="overwrite_partitions",
        )
        logger.info(
            f"saved year={data_date:%Y}/month={data_date:%m} "
            f"on {data_date} to {s3_bucket}"
        )
    else:
        logger.info(f"no data on {data_date.isoformat()}")


###################
# Commands
###################

TODAY = dt.date.today()
LAST_2_WEEKS = TODAY - relativedelta(weeks=2)
S3_BUCKET = "s3://noos-prod-neptune-services/"

if __name__ == "__main__":

    if LAST_2_WEEKS.month != TODAY.month:
        save_enedis_main_profiles_act(
            dataset="coefficients-des-profils",
            data_date=LAST_2_WEEKS,
            s3_bucket=S3_BUCKET,
        )

    save_enedis_main_profiles_act(
        dataset="coefficients-des-profils",
        data_date=TODAY,
        s3_bucket=S3_BUCKET,
    )
