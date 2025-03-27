import requests

from utils import sanitize_filename
from vars import *



class Modrinth:
    user_agent = MODRINTH_USER_AGENT.format(GITHUB_USERNAME, PROJECT_NAME, VERSION, CONTACT)
    headers = {"User-Agent": user_agent}

    @staticmethod
    def get_project(project_id: str) -> dict:
        """Fetches project data from Modrinth by project ID."""
        response = requests.get(f"{MODRINTH_BASE_URL}/project/{project_id}", headers=Modrinth.headers)
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def get_projects(project_ids: list[str]) -> list[dict]:
        """Fetches projects data from Modrinth by project IDs."""
        response = requests.post(f"{MODRINTH_BASE_URL}/projects", json={"ids": project_ids}, headers=Modrinth.headers)
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def get_version(version_id: str) -> dict:
        """Fetches version data from Modrinth by version ID."""
        response = requests.get(f"{MODRINTH_BASE_URL}/version/{version_id}", headers=Modrinth.headers)
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def get_versions(version_ids: list[str]) -> list[dict]:
        """Fetches versions data from Modrinth by version IDs."""
        response = requests.post(f"{MODRINTH_BASE_URL}/versions", json={"ids": version_ids}, headers=Modrinth.headers)
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def get_dependencies(version: dict) -> list:
        """Extracts a list of required dependencies from a version dictionary."""
        required = []
        for dep in version["dependencies"]:
            if dep["dependency_type"] == "required":
                required.append(sanitize_filename(Modrinth.get_project(dep["project_id"])["title"]))
        return required
