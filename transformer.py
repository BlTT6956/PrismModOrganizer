from typing import Dict, List, Optional
from datetime import datetime

from setting import settings
from vars import BROKEN_IMAGE_ICON, MODRINTH_MOD_URL
from utils import sanitize_filename
from converter import curseforge_to_modrinth


def format_date(date_str: Optional[str]) -> Optional[str]:
    """Formats the date string into a readable format."""
    if not date_str:
        return None
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_obj.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return None

def format_link(value) -> list | str:
    if isinstance(value, str):
        return f"[[{value}]]"
    elif isinstance(value, list):
        return [f"[[{item}]]" for item in value]

def from_platform(
    local_data: dict,
    enabled: bool = True,
    project_data: Optional[Dict] = None,
    version_data: Optional[Dict] = None,
    dependencies: Optional[List[Dict]] = None,
    remove_empty: bool = True,
    ) -> Dict:
    """Transforms data based on the platform (CurseForge or Modrinth) into a unified format."""

    project_data = project_data or {}
    version_data = version_data or {}
    dependencies = dependencies or []
    result = {}

    platform = next(iter(local_data.get("update")))
    filename = local_data["filename"].removesuffix(".jar")

    base_data = {
        "Name": sanitize_filename(local_data["name"]),
        "Stem": filename,
        "Enabled": enabled,
        "Platform": platform,
        "Side": local_data["side"],
        "Categories": [],
        "Loaders": local_data["x-prismlauncher-loaders"],
        "Game versions": local_data["x-prismlauncher-mc-versions"],
        "Release type": local_data["x-prismlauncher-release-type"],
        "Dependencies": format_link(dependencies),
        "Description": "Failed to fetch mod description",
        "Downloads": None,
        "Followers": None,
        "Version name": version_data.get("displayName"),
        "Version number": None,
        "Version date": format_date(version_data.get("fileDate")),
        "Version type": None,
        "Changelog": None,
        "File update": local_data["Date"],
    }

    if platform == "curseforge":
        result = {
            **base_data,
            "Project ID": local_data["update"]["curseforge"].get("project-id"),
            "Version ID": local_data["update"]["curseforge"].get("file-id"),
            "Description": project_data.get("summary", base_data["Description"]),
            "Downloads": project_data.get("downloadCount", base_data["Downloads"]),
            "Followers": base_data["Followers"],
            "Slug": project_data.get("slug"),
            "Categories": [curseforge_to_modrinth(category["name"]) for category in project_data.get("categories", [])],
            "Icon": project_data.get("logo", {}).get("url", BROKEN_IMAGE_ICON),
            "Site URL": project_data.get("links", {}).get("websiteUrl"),
            "Source URL": project_data.get("links", {}).get("sourceUrl"),
            "Issues URL": project_data.get("links", {}).get("issuesUrl"),
            "Wiki URL": project_data.get("links", {}).get("wikiUrl"),
            "Version name": version_data.get("displayName"),
            "Version date": format_date(version_data.get("fileDate")),
        }

    elif platform == "modrinth":
        slug = project_data.get("slug")

        result = {
            **base_data,
            "Project ID": local_data["update"]["modrinth"].get("mod-id"),
            "Version ID": local_data["update"]["modrinth"].get("version"),
            "Description": project_data.get("description", base_data["Description"]),
            "Downloads": project_data.get("downloads", base_data["Downloads"]),
            "Followers": project_data.get("followers", base_data["Followers"]),
            "Slug": slug,
            "Categories": project_data.get("categories", []),
            "Icon": project_data.get("icon_url", BROKEN_IMAGE_ICON),
            "Site URL": f"{MODRINTH_MOD_URL}/{slug}" if slug else None,
            "Source URl": project_data.get("source_url"),
            "Issues URl": project_data.get("issues_url"),
            "Wiki URl": project_data.get("wiki_url"),
            "Version name": version_data.get("name"),
            "Version number": version_data.get("version_number"),
            "Version date": format_date(version_data.get("date_published")),
            "Version type": version_data.get("version_type"),
            "Changelog": version_data.get("changelog"),
        }

    else:
        raise ValueError("Unsupported platform")

    result = {
        **result,
        "Tags": result["Categories"]
    }

    if remove_empty:
        result = {k: v for k, v in result.items() if v is not None}
    return result