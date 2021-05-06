import datetime
import logging
import logging.config
import os
from functools import wraps
from typing import Dict

import pandas as pd
import yaml

__all__ = ["setup_logging", "hive_parquet_save", "rounddown_time", "log_args"]


###################
# Logging
###################


def setup_logging(
    default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"
):
    """**@author:** Prathyush SP | Logging Setup."""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print("Failed to load configuration file. Using default configs")


logger = logging.getLogger(__name__)
setup_logging()


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


def hive_parquet_save(
    df: pd.DataFrame,
    s3_bucket: str,
    hive_partitions: Dict[str, str],
) -> None:
    """Save a dataframe in a partitioned parquet.

    :param df: dataframe to save
    :param s3_bucket: s3 bucket including store path
    :param hive_partitions: dictionary of partitions.
            Example: {
                'type': 'WEATHER',
                'asset': 'T_2M',
                'category': 'ARPEGE',
                'settlement_run': 'PREV',
                'created_at': '20210501T06:00:00',
                }
    :return: None
    """
    for key, value in hive_partitions.items():
        df[key] = value

    parquet_params = {
        "index": False,
        "engine": "pyarrow",
        "compression": "snappy",
    }
    df.to_parquet(
        s3_bucket, partition_cols=list(hive_partitions.keys()), **parquet_params
    )


def rounddown_time(dt=None, timedelta=datetime.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta.

    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    round_to = timedelta.total_seconds()

    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = seconds // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)
