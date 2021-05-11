import datetime
import logging
import logging.config
import os
from functools import wraps
from typing import Dict

import awswrangler as wr
import numpy as np
import pandas as pd
import yaml
from sklearn.impute import KNNImputer

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

# Not working without s3fs
def hive_pandas_parquet_save(
    df: pd.DataFrame,
    s3_bucket: str,
    hive_partitions: Dict[str, str],
    df_columns_type: Dict[str, str],
) -> None:
    """Save a dataframe in a partitioned parquet.

    :param df: dataframe to save
    :param df_columns_type: dictionary of columns to keep with type (order matters)
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
    df = df[list(df_columns_type.keys())].astype(df_columns_type)
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


def setup_wrangler():
    # https://github.com/awslabs/aws-data-wrangler/blob/
    # 2da313473e6426128fff0111ae819fb55ccc87ee/tutorials/021%20-%20Global%20Configurations.ipynb
    pass


def datalake_wrangler_save(
    df: pd.DataFrame,
    s3_bucket: str,
    hive_partitions: Dict[str, str],
    df_columns_type: Dict[str, str] = None,
    mode: str = "append",
    # database: str,
    # table: str,
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
    :param df_columns_type: dictionary of columns to keep with type (order matters)
    :param mode: default `overwrite_partitions` to append to existing dataset avoiding duplicates
    :return: None
    """
    setup_wrangler()

    # Athena dtype are specific: https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    if df_columns_type is not None:
        df = df[list(df_columns_type.keys())].astype(df_columns_type)
    for key, value in hive_partitions.items():
        df[key] = value

    parquet_params = {
        "index": False,
        "compression": "snappy",
        "dataset": True,
        "mode": mode,
        "partition_cols": list(hive_partitions.keys()),
        "use_threads": True,
    }

    wr.s3.to_parquet(df=df, path=s3_bucket, **parquet_params)


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


def interpolate_to_freq(df: pd.DataFrame, freq: str = "30T") -> pd.DataFrame:
    # Linear interpolation as performed by enedis
    index = pd.date_range(
        start=df.index.min(), end=df.index.max(), freq=freq, name="delivery_from"
    )
    return df.reindex(index).interpolate(method="linear", axis=0)


def fill_missing_values(pivot_df: pd.DataFrame) -> pd.DataFrame:
    # Looking at the 4 closest stations in distance (t wise) to fill gaps
    imputer = KNNImputer(n_neighbors=4, weights="distance")

    return pd.DataFrame(
        imputer.fit_transform(
            pivot_df.transpose().to_numpy(dtype="float", na_value=np.nan)
        ).transpose(),
        columns=pivot_df.columns,
        index=pivot_df.index,
    )
