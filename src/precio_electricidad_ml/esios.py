import requests

TOKEN = "1b6edff118e8b67af659702f3f89aef846b9e3452ef795f3008885c5780c4a46"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-api-key": TOKEN
}

URL = "https://api.esios.ree.es/indicators/"

def request_esios_indicator(indicator, params={}):
    response = requests.get(
        URL + str(indicator), 
        headers=headers, 
        params=params,
        verify=False
    )

    return response.json()