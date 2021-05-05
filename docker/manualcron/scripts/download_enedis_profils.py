import datetime as dt
import logging
from functools import wraps
from io import BytesIO
from typing import Dict

import click
import pandas as pd
import requests
from click import types as click_types
from dateutil import relativedelta

###################
# Logging
###################


logger = logging.getLogger(__name__)


def log_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log pre-processing
        msg = f"Starting {func.__name__} command "
        msg += "".join([f"{key}: {str(value)} " for key, value in kwargs.items()])
        logger.info(msg)

        # Function call
        func(*args, **kwargs)

        # Log post-processing
        logger.info(f"Completing {func.__name__} command")

    return wrapper


###################
# Functions
###################


def download_enedis_data(dataset: str, params: Dict["str", "str"]) -> pd.DataFrame:
    api_url = "https://data.enedis.fr/api/v2/catalog/datasets/"

    payload = {"limit": "-1", "timezone": "UTC"}
    payload.update(params)

    r = requests.get(f"{api_url}{dataset}/exports/csv?", params=payload)

    columns_types = {
        "horodate": "str",
        "sous_profil": "str",
        "categorie": "str",
        "coefficient_prepare": "float",
        "coefficient_ajuste": "float",
        "coefficient_dynamique": "float",
    }

    if r.status_code == 200:
        df = pd.read_csv(BytesIO(r.content), delimiter=";", dtype=columns_types)
        return df
    else:
        raise SyntaxError(r.status_code)


def save_enedis_main_profils_data(
    dataset: str, data_date: dt.date, s3_bucket: str
) -> str:
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

    parquet_params = {
        "index": False,
        "engine": "pyarrow",
        "compression": "snappy",
    }

    params = dict()
    params__date = {"refine": f"horodate:{data_date.isoformat()}"}
    params.update(params__date)
    params__profils = {"where": " OR ".join(f'"{w}"' for w in dynamic_profiles)}
    params.update(params__profils)

    df = download_enedis_data(dataset, params)

    filename = f"{dataset}/date={data_date.isoformat()}/data.parquet"
    if not df.empty:
        df.to_parquet(s3_bucket + filename, **parquet_params)

        return f"saved {filename} to {s3_bucket}"
    else:
        return f"no data on {data_date.isoformat()}"


###################
# Commands
###################

__all__ = [
    "save_enedis_main_profils_data_command",
]

TODAY = dt.date.today()
S3_BUCKET = "s3://noos-prod-neptune-services/Raw/ENEDIS/"

DATETIME_FORMAT = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]


@click.command(name="save-enedis-main-profils-data")
@click.option("--dataset", help="ENEDIS dataset to download", required=True, type=str)
@click.option(
    "--published-for",
    help="Reference datetime for the data",
    type=click_types.DateTime(formats=DATETIME_FORMAT),
    default=TODAY.isoformat(),
)
@click.option("--s3-bucket", help="S3 bucket to save data", type=str, default=S3_BUCKET)
@log_args
def save_enedis_main_profils_data_command(
    dataset: str,
    published_for: dt.datetime,
    s3_bucket: str,
):
    """Fetch Meteo France synop data and save chosen parameters to s3 bucket."""
    msg = save_enedis_main_profils_data(
        dataset=dataset, data_date=published_for.date(), s3_bucket=s3_bucket
    )
    logger.info(msg)


last_week = TODAY - relativedelta.relativedelta(days=7)

if __name__ == "__main__":

    save_enedis_main_profils_data(
        dataset="coefficients-des-profils",
        data_date=last_week,
        s3_bucket=S3_BUCKET,
    )
    save_enedis_main_profils_data(
        dataset="coefficients-de-profils-dynamiques-anticipes-en-j1",
        data_date=TODAY,
        s3_bucket=S3_BUCKET,
    )
