import datetime as dt
import logging
import os
from functools import wraps

import click
import pandas as pd
import pytz
import requests
from click import types as click_types

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
# RTE functions
###################


def requestToken(rte_token):
    """OAuth v.2 token request to RTE identification server.

    :return: a token valid for 2 hours.
    """
    header = {"Authorization": "Basic " + rte_token}
    r = requests.post(
        "https://digital.iservices.rte-france.com/token/oauth/", headers=header
    )
    if r.status_code == requests.codes.ok:
        access_token = r.json()["access_token"]
        # print('Gathered token : ' + access_token)
        return access_token
    else:
        return ""


def headerWithToken(temp_token):
    return {"Authorization": "Bearer " + temp_token}


def param_dates_str(start_date: dt.datetime, end_date: dt.datetime):
    return f"start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"


def get_ccr(publication_date: dt.date, rte_token: str) -> pd.DataFrame:
    """Retrieve Certified Capacities Registry."""
    rte_api_url = "https://digital.iservices.rte-france.com/open_api/"
    rte_api_endpoint = "certified_capacities_registry/v1/"
    rte_ncc = ["ncc_less_100_mw", "ncc_greater_equal_100_mw"]

    start_date = dt.datetime(
        publication_date.year - 2, 1, 1, tzinfo=pytz.timezone("CET")
    )
    end_date = dt.datetime(publication_date.year + 4, 1, 1, tzinfo=pytz.timezone("CET"))

    capacity_df = pd.DataFrame()
    for ncc in rte_ncc:
        r = requests.get(
            rte_api_url + rte_api_endpoint + ncc,
            params=param_dates_str(start_date, end_date),
            headers=headerWithToken(requestToken(rte_token)),
        )
        if r.status_code == 200:
            temp_df = pd.json_normalize(r.json()[ncc])
            capacity_df = pd.concat([capacity_df, temp_df], ignore_index=True)
        else:
            raise SyntaxError(r.status_code)

    capacity_df["publication_date"] = TODAY

    return capacity_df


def save_ccr(publication_date: dt.date, rte_token: str, s3_bucket: str) -> str:
    capacity_df = get_ccr(publication_date=publication_date, rte_token=rte_token)

    filename = f"certified_capacities_registry/{publication_date.isoformat()}.parquet"
    capacity_df.to_parquet(s3_bucket + filename)

    return f"{filename} created in: {s3_bucket}"


###################
# Commands
###################

__all__ = [
    "save_ccr_command",
]

TODAY = dt.date.today()
RTE_TOKEN = os.getenv("RTE_ID64")
S3_BUCKET = "s3://noos-prod-neptune-services/Raw/RTE/"

DATETIME_FORMAT = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]


@click.command(name="save-ccr")
@click.option(
    "--published-at",
    help="Reference datetime for the save",
    type=click_types.DateTime(formats=DATETIME_FORMAT),
    default=TODAY.isoformat(),
)
@click.option(
    "--rte-token", help="RTE app token to authentify", type=str, default=RTE_TOKEN
)
@click.option("--s3-bucket", help="S3 bucket to save data", type=str, default=S3_BUCKET)
@log_args
def save_ccr_command(
    published_at: dt.datetime,
    rte_token: str,
    s3_bucket: str,
):
    """Fetch CCR and save to s3 bucket."""
    msg = save_ccr(
        publication_date=published_at.date(), rte_token=rte_token, s3_bucket=s3_bucket
    )
    logger.info(msg)


if __name__ == "__main__":
    save_ccr_command()
