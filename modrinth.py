from setting import *
import requests
from utils import sanitize_filename


class Modrinth:
    user_agent = MODRINTH_USER_AGENT.format(GITHUB_USERNAME, PROJECT_NAME, VERSION, CONTACT)
    headers = {"User-Agent": user_agent}

    @staticmethod
    def get_project(project_id: str) -> dict:
        """Fetches project data from Modrinth by project ID."""
        response = requests.get(MODRINTH_PROJECT.format(project_id), headers=Modrinth.headers)
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_version(version_id: str) -> dict:
        """Fetches version data from Modrinth by version ID."""
        response = requests.get(MODRINTH_VERSION.format(version_id), headers=Modrinth.headers)
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_dependencies(version: dict) -> list:
        """Extracts a list of required dependencies from a version dictionary."""
        result = []
        for dep in version["dependencies"]:
            if dep["dependency_type"] == "required":
                result.append(sanitize_filename(Modrinth.get_project(dep["project_id"])["title"]))
        return result
