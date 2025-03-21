from dynaconf import settings
import requests


def fetch_mod_data(mod_id: str) -> dict:
    response = requests.get(settings["modrinth"]["url"].format(mod_id))
    if response.status_code == 200:
        return response.json()


fetch_mod_data("fX4dIQCo")