import requests


def request_token(rte_token):
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


def header_with_token(rte_token):
    temp_token = request_token(rte_token)
    return {"Authorization": "Bearer " + temp_token}
