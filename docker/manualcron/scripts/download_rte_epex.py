import os

import click
import logging
import pandas as pd
import requests
import utils

import utils_rte

###################
# Logging
###################

logger = logging.getLogger(__name__)
utils.setup_logging()


def get_epex(rte_token: str) -> pd.DataFrame:
    """Retrieve Certified Capacities Registry."""
    rte_api_url_global = "https://digital.iservices.rte-france.com/open_api/"
    rte_api_url_endpoint = "wholesale_market/v2/"
    rte_api_endpoint = "france_power_exchanges"

    df = pd.DataFrame()

    request = rte_api_url_global + rte_api_url_endpoint + rte_api_endpoint
    headers = utils_rte.header_with_token(rte_token)

    r = requests.get(
        request,
        headers=headers,
    )
    if r.status_code == 200:
        df = pd.json_normalize(r.json()[rte_api_endpoint][0]["values"])
        df["updated_date"] = r.json()[rte_api_endpoint][0]["updated_date"]
    else:
        raise SyntaxError(r.status_code)

    return df


def save_epex(rte_token: str, s3_bucket: str) -> str:
    df = get_epex(rte_token=rte_token)

    df["delivery_from"] = pd.to_datetime(df.start_date, utc=True)
    df["published_at"] = pd.to_datetime(df.updated_date, utc=True)

    filename = f"epex_spot/{df.published_at[0].date().isoformat()}.parquet"
    df.to_parquet(s3_bucket + filename)

    return f"{filename} created in: {s3_bucket}"


###################
# Commands
###################

RTE_TOKEN = os.getenv("RTE_ID64")
S3_BUCKET = "s3://noos-prod-neptune-services/Raw/RTE/"


@click.command(name="save-epex")
@click.option(
    "--rte-token", help="RTE app token to authentify", type=str, default=RTE_TOKEN
)
@click.option("--s3-bucket", help="S3 bucket to save data", type=str, default=S3_BUCKET)
@utils.log_args
def save_epex_command(
    rte_token: str,
    s3_bucket: str,
):
    """Fetch epex spot and save to s3 bucket."""
    msg = save_epex(rte_token=rte_token, s3_bucket=s3_bucket)
    logger.info(msg)


if __name__ == "__main__":
    save_epex_command()
