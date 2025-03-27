import requests

import keyring

from vars import *
from utils import sanitize_filename


class CurseForge:
    @staticmethod
    def get_project(project_id: str, api: str = None) -> dict:
        """Fetches project data from Modrinth by project ID."""
        api = api or CurseForge.get_api_key()
        response = requests.get(f"{CURSEFORGE_BASE_URL}/{project_id}", headers={"x-api-key": api})
        return response.json()["data"] if response.status_code == 200 else {}

    @staticmethod
    def get_projects(project_ids: list[str], api: str = None) -> list[dict]:
        """Fetches multiple projects data from CurseForge by project IDs."""
        api = api or CurseForge.get_api_key()
        response = requests.post(f"{CURSEFORGE_BASE_URL}/mods", json={"modIds": project_ids}, headers={"x-api-key": api})
        return response.json()["data"] if response.status_code == 200 else {}

    @staticmethod
    def get_version(project_id: str, version_id: str, api: str = None) -> dict:
        """Fetches version data from Modrinth by version ID."""
        api = api or CurseForge.get_api_key()
        response = requests.get(f"{CURSEFORGE_BASE_URL}/{project_id}/files/{version_id}", headers={"x-api-key": api})
        return response.json()["data"] if response.status_code == 200 else {}

    @staticmethod
    def get_versions(project_id: str, version_ids: list[str], api: str = None) -> list[dict]:
        """Fetches multiple versions data from CurseForge by version IDs."""
        api = api or CurseForge.get_api_key()
        response = requests.post(
            f"{CURSEFORGE_BASE_URL}/mods/{project_id}/files",
            json={"fileIds": version_ids},
            headers={"x-api-key": api},
        )
        return response.json()["data"] if response.status_code == 200 else {}

    @staticmethod
    def get_dependencies(version: dict, api: str = None) -> list:
        """Extracts a list of required dependencies from a version dictionary."""
        api = api or CurseForge.get_api_key()
        result = []
        if not version:
            return result
        for dep in version["dependencies"]:
            if dep["relationType"] == 3:
                result.append(sanitize_filename(CurseForge.get_project(dep["modId"], api)["name"]))
        return result

    @staticmethod
    def save_api_key():
        """Asks the user for an API key and stores it in the OS keyring."""
        api_key = input("Enter CurseForge API key: ")
        keyring.set_password("PrismObsidian", "PrismObsidian", api_key)
        return api_key

    @staticmethod
    def get_api_key() -> str:
        """Retrieves the API key from the OS keyring."""
        return keyring.get_password("PrismObsidian", "PrismObsidian") or CurseForge.save_api_key()