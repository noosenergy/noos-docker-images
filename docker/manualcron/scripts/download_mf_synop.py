import datetime as dt
import logging
from functools import wraps

import click
import pandas as pd
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
# Functions
###################

# Downloads raw data from mf server. Data available in H+3 every 3h
def save_mf_synop_data(data_date: dt.datetime, s3_bucket: str):
    # Source
    root_url = (
        "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/"
    )

    parquet_params = {
        "index": False,
        "engine": "pyarrow",
        "compression": "snappy",
    }

    columns_types = {
        "numer_sta": "str",
        "date": "str",
        "pmer": "int",
        "tend": "int",
        "cod_tend": "int",
        "dd": "int",
        "ff": "float",
        "t": "float",
        "td": "float",
        "u": pd.Int64Dtype(),
        "vv": "float",
        "ww": "int",
        "w1": "int",
        "w2": "int",
        "n": "float",
        "nbas": "int",
        "hbas": "int",
        "cl": "int",
        "cm": "int",
        "ch": "int",
        "pres": pd.Int64Dtype(),
        "niv_bar": "int",
        "geop": "int",
        "tend24": "int",
        "tn12": "float",
        "tn24": "float",
        "tx12": "float",
        "tx24": "float",
        "tminsol": "float",
        "sw": "int",
        "tw": "float",
        "raf10": "float",
        "rafper": "float",
        "per": "float",
        "etat_sol": "int",
        "ht_neige": "float",
        "ssfrai": "float",
        "perssfrai": "float",
        "rr1": "float",
        "rr3": "float",
        "rr6": "float",
        "rr12": "float",
        "rr24": "float",
        "phenspe1": "float",
        "phenspe2": "float",
        "phenspe3": "float",
        "phenspe4": "float",
        "nnuage1": "int",
        "ctype1": "int",
        "hnuage1": "int",
        "nnuage2": "int",
        "ctype2": "int",
        "hnuage2": "int",
        "nnuage3": "int",
        "ctype3": "int",
        "hnuage3": "int",
        "nnuage4": "int",
        "ctype4": "int",
        "hnuage4": "int",
    }

    columns_to_keep = ["numer_sta", "date", "t", "ff", "u", "pres"]
    filename = f"synop.{data_date:%Y}{data_date:%m}.csv.gz"

    data = pd.read_csv(
        root_url + filename,
        delimiter=";",
        header=0,
        na_values="mq",
        usecols=columns_to_keep,
        dtype=columns_types,
    ).dropna(axis="columns", how="all")
    clean_data = data.drop_duplicates()
    clean_data.to_parquet(
        s3_bucket + f"synop/YEAR={data_date:%Y}/MONTH={data_date:%m}/synop.parquet",
        **parquet_params,
    )
    nb_duplicates = data.duplicated().sum()
    return (
        f"{filename} synced in: {s3_bucket}"
        f"{f' ... found {nb_duplicates} duplicates' if nb_duplicates>0 else ''}"
    )


###################
# Commands
###################

__all__ = [
    "save_mf_synop_data_command",
]

TODAY = dt.date.today()
S3_BUCKET = "s3://noos-prod-neptune-services/Raw/METEOFRANCE/"

DATETIME_FORMAT = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]


@click.command(name="save-mf-synop-data")
@click.option(
    "--published-for",
    help="Reference datetime for the data",
    type=click_types.DateTime(formats=DATETIME_FORMAT),
    default=TODAY.isoformat(),
)
@click.option("--s3-bucket", help="S3 bucket to save data", type=str, default=S3_BUCKET)
@log_args
def save_mf_synop_data_command(
    published_for: dt.datetime,
    s3_bucket: str,
):
    """Fetch Meteo France synop data and save chosen parameters to s3 bucket."""
    msg = save_mf_synop_data(data_date=published_for.date(), s3_bucket=s3_bucket)
    logger.info(msg)


if __name__ == "__main__":
    save_mf_synop_data_command()
