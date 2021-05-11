import logging
from io import BytesIO
from typing import Dict

import pandas as pd
import requests
import utils

###################
# Logging
###################


logger = logging.getLogger(__name__)
utils.setup_logging()


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
