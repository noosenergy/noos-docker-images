import datetime as dt
import logging

import awswrangler as wr
import click
import utils
import utils_enedis
from click import types as click_types
from utils import log_args

###################
# Logging
###################


logger = logging.getLogger(__name__)
utils.setup_logging()


###################
# Functions
###################


def save_enedis_main_profiles_prov(
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
    params__date = {"refine": f"horodate:{data_date.isoformat()}"}
    params.update(params__date)
    params__profils = {"where": " OR ".join(f'"{w}"' for w in dynamic_profiles)}
    params.update(params__profils)

    df = utils_enedis.download_enedis_data(dataset, params)

    if not df.empty:
        wr.s3.to_parquet(
            df=df.drop_duplicates(),
            path=f"{s3_bucket}Raw/ENEDIS/{dataset}/date={data_date.isoformat()}/",
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

YESTERDAY = dt.date.today() - dt.timedelta(days=1)
S3_BUCKET = "s3://noos-prod-neptune-services/"

DATETIME_FORMAT = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]


@click.command(name="save-enedis-main-profils-data")
@click.option("--dataset", help="ENEDIS dataset to download", required=True, type=str)
@click.option(
    "--published-for",
    help="Reference datetime for the data",
    type=click_types.DateTime(formats=DATETIME_FORMAT),
    default=YESTERDAY.isoformat(),
)
@click.option("--s3-bucket", help="S3 bucket to save data", type=str, default=S3_BUCKET)
@log_args
def save_enedis_main_profiles_prov_command(
    dataset: str,
    published_for: dt.datetime,
    s3_bucket: str,
):
    """Fetch Meteo France synop data and save chosen parameters to s3 bucket."""
    save_enedis_main_profiles_prov(
        dataset=dataset, data_date=published_for.date(), s3_bucket=s3_bucket
    )


if __name__ == "__main__":

    save_enedis_main_profiles_prov(
        dataset="coefficients-de-profils-dynamiques-anticipes-en-j1",
        data_date=YESTERDAY,
        s3_bucket=S3_BUCKET,
    )
