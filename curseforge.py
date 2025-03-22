from setting import *
import requests
from utils import sanitize_filename


class CurseForge:
    @staticmethod
    def get_project(project_id: str, api: str) -> dict:
        """Fetches project data from Modrinth by project ID."""
        response = requests.get(CURSEFORGE_PROJECT.format(project_id), headers={"x-api-key": api})
        if response.status_code == 200:
            return response.json()["data"]

    @staticmethod
    def get_version(project_id: str, version_id: str, api: str) -> dict:
        """Fetches version data from Modrinth by version ID."""
        response = requests.get(CURSEFORGE_VERSION.format(project_id, version_id), headers={"x-api-key": api})
        if response.status_code == 200:
            return response.json()["data"]

    @staticmethod
    def get_dependencies(version: dict, api: str) -> list:
        """Extracts a list of required dependencies from a version dictionary."""
        result = []
        for dep in version["dependencies"]:
            if dep["relationType"] == 3:
                result.append(sanitize_filename(CurseForge.get_project(dep["modId"], api)["name"]))
        return result

