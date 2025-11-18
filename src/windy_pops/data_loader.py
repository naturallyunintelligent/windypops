import argparse
import json
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Any

import attrs
import requests

from windy_pops.constants import DATA_DIR, SECRETS_PATH


def Metoffice_dataloader():
    return DataLoader.from_api("met_office_datahub")


@attrs.frozen
class DataLoader:
    _data: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path) -> "DataLoader":
        with path.open("r") as file:
            data = json.load(
                file
            )  # try-except block?
            return DataLoader(data=data)

    @classmethod
    def from_api(cls, api_key: str) -> "DataLoader":
        met_key = _get_api_key(api_key, "global_spot_api_key")

        # met_Datahub_api_base = 
        # "https://data.hub.api.metoffice.gov.uk/sitespecific/v0"
        # met_Datahub_api_request = "/point/three-hourly"
        # met_Datahub_api_forecast_url = 
        # f"{met_Datahub_api_base}{met_Datahub_api_request}?dataSource=BD1&includeLocationName=true&latitude={shoreham_beach['lat']}&longitude={shoreham_beach['long']}"
        met_Datahub_api_base = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0"
        met_Datahub_api_request = "/point/three-hourly"
        latitude = 50.827274
        longitude = -0.271525
        met_Datahub_api_forecast_url = (
            f"{met_Datahub_api_base}{met_Datahub_api_request}"
            f"?dataSource=BD1&includeLocationName=true"
            f"&latitude={latitude}&longitude={longitude}"
        )

        # response = requests.get(met_Datahub_api_forecast_url, headers={"accept": "application/json", "apikey": "<keypastedhere>"})
        headers = {"accept": "application/json", "apikey": met_key}
        try:
            response = requests.get(met_Datahub_api_forecast_url, headers)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err)
            # the rest of my code is going here
        data = response.json()
        return DataLoader(data=data)

    @classmethod
    def from_latest_cache(cls, cache_dir: Path) -> "DataLoader":
        latest_cached_file = _get_latest_file(cache_dir=cache_dir)
        with latest_cached_file.open("r") as file:
            data = json.load(
                file
            )  # could put this in a try-except block to catch errors gracefully
            return DataLoader(data=data)

    def to_file(
        self, path: Path
    ) -> None:  # may want to check if the data is empty before writing it?
        with path.open("w") as file:
            json.dump(self.data, fp=file, indent=4)

    def cache(self, cache_dir: Path = DATA_DIR) -> None:
        output_path = (
            cache_dir / f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}_response.json"
        )
        self.to_file(output_path)

    @property
    def data(self) -> dict[str, Any]:
        return self._data


def _get_api_key(section, property):
    """Fetch the API key from your configuration file.

    Expects a configuration file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>

    where the section is openweather and the property is api_key in the example above
    """
    if not SECRETS_PATH.exists():
        raise FileNotFoundError("secrets.ini file not found")
    config = ConfigParser()
    config.read(SECRETS_PATH)
    return config[section][property]


def _get_latest_file(cache_dir=DATA_DIR) -> Path:
    if not cache_dir.exists():
        raise FileNotFoundError("data directory not found")
    data_paths = cache_dir.glob("*_response.json")
    return max(data_paths, key=lambda path: path.stat().st_ctime)


# def get_weather_forecast(use_cache, cached_data_file=None):
#     # Weather Forecast
#     met_key = _get_api_key("met_office_datahub", "global_spot_api_key")
#
#     met_Datahub_api_base = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0"
#     met_Datahub_api_request = "/point/three-hourly"
#     #met_Datahub_api_forecast_url = f"{met_Datahub_api_base}{met_Datahub_api_request}?dataSource=BD1&includeLocationName=true&latitude={shoreham_beach['lat']}&longitude={shoreham_beach['long']}"
#     met_Datahub_api_forecast_url = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/three-hourly?dataSource=BD1&includeLocationName=true&latitude=50.827274&longitude=-0.271525"
#
#     # response = requests.get(met_Datahub_api_forecast_url, headers={"accept": "application/json", "apikey": "<keypastedhere>"})
#     # or better:
#     headers = {"accept": "application/json", "apikey": met_key}
#
#     if not use_cache:
#         # https://3.python-requests.org/api/#requests.Response.raise_for_status
#         # https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testing
#         try:
#             response = requests.get(met_Datahub_api_forecast_url, headers)
#             response.raise_for_status()
#         except requests.exceptions.ConnectionError as err:
#             # eg, no internet
#             raise SystemExit(err)
#         except requests.exceptions.HTTPError as err:
#             # eg, url, server and other errors
#             raise SystemExit(err)
#             # the rest of my code is going here
#
#         data = response.json()
#         datetime_now = datetime.now()
#         # save the data as a text file for local dev:
#         with open(f"{DATA_DIR}/{datetime_now.strftime('%Y-%m-%d-%H-%M-%S')}.json", "w") as file:
#             file.write(response.text)
#
#     else:
#         if cached_data_file is None:
#             cached_data_file = _get_latest_file()
#         with open(f"{DATA_DIR}/{cached_data_file}", "r") as file:
#             data = json.load(file)
#
#
#
#     return data


# geojson?

# Weather - Current weather conditions


# Tides - High and Low tide times
# -> float of tide height


# Waves - Swell and Wind
# -> float of swell height


# Daylight - Sunrise and Sunset times to give a boolean value of whether it is light or dark
# -> boolean value of whether it is light or dark


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", default={"lat": "50.827274", "long": "-0.271525"})
    data_source = parser.add_mutually_exclusive_group(required=True)
    data_source.add_argument(
        "--api",
        action="store_true",
        default=False,
        help="Get the latest data from the API",
    )
    data_source.add_argument(
        "--latest-cached",
        action="store_true",
        default=False,
        help="Use the most recently cached data",
    )
    data_source.add_argument("--file", nargs=1, help="Path to input data file")
    args = parser.parse_args()

    data_loader = DataLoader.from_latest_cache()
    print(data_loader.data)
