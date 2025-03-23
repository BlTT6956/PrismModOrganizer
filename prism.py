from pathlib import Path
import pprint
from curseforge import CurseForge
from modrinth import Modrinth
import toml
from tqdm import tqdm
import os
from utils import sanitize_filename, get_api_key, get_stem


class Prism:
    def __init__(self, instance, obsidian):
        """Initialize the Prism instance by selecting an instance."""
        self.instance = instance
        self.obsidian = obsidian

    @property
    def data(self) -> list[dict]:
        """Load and return a list of mod data from .pw.toml files."""
        result = []
        for path in tqdm(self.toml, desc="Loading..."):
            if res := self.single_data(path):
                result.append(res)
        return result

    @property
    def local_data(self) -> list[dict]:
        result = []
        for path in self.toml:
            data = self.local_single_data(path)
            result.append(data)
        return result

    def local_single_data(self, path: Path) -> dict:
        data = toml.loads(path.read_text(encoding="utf-8"))
        data["name"] = sanitize_filename(data["name"])
        data["enabled"] = data["filename"] in [p.name for p in self.enabled_mods]
        data["path"] = path
        return data

    def single_data(self, path: Path | str, anyway=False) -> dict | None:
        """Get mod details from a .ps.toml file and Modrinth. Returns a dictionary or None if no data is found."""
        data = toml.loads(path.read_text(encoding="utf-8"))
        data["name"] = sanitize_filename(data["name"])
        data["path"] = Path(path)
        if self.obsidian.check_md(data) and not anyway:
            return None
        data["enabled"] = data["filename"] in [p.name for p in self.enabled_mods]
        if data["update"].get("modrinth"):
            data["platform"] = "modrinth"
            data["project"] = Modrinth.get_project(data["update"]["modrinth"]["mod-id"])
            data["version"] = Modrinth.get_version(data["update"]["modrinth"]["version"])
            data["dependencies"] = Modrinth.get_dependencies(data["version"])
        else:
            data["platform"] = "curseforge"
            data["project"] = CurseForge.get_project(data["update"]["curseforge"]["project-id"], get_api_key())
            data["version"] = CurseForge.get_version(data["update"]["curseforge"]["project-id"], data["update"]["curseforge"]["file-id"], get_api_key())
            data["dependencies"] = CurseForge.get_dependencies(data["version"], get_api_key())
            data["project"]["description"] = data["project"]["summary"]
            data["project"]["downloads"] = data["project"]["downloadCount"]
            data["project"]["followers"] = 0
            modrinth = Modrinth.get_project(data["project"]["slug"])
            if "Client" in data["version"]["gameVersions"] and "Server" in data["version"]["gameVersions"]:
                data["side"] = "both"
            elif "Client" in data["version"]["gameVersions"]:
                data["side"] = "client"
            elif "Server" in data["version"]["gameVersions"]:
                data["side"] = "server"
            else:
                data["side"] = "both"
            if modrinth:
                data["project"]["server_side"] = modrinth["server_side"]
                data["project"]["client_side"] = modrinth["client_side"]
            else:
                data["project"]["server_side"] = "None"
                data["project"]["client_side"] = "None"
            data["project"]["icon_url"] = data["project"]["logo"]["url"]
            data["project"]["categories"] = [d["name"] for d in data["project"]["categories"]]
        return data

    @property
    def toml(self) -> list[Path]:
        """Return a list of .pw.toml files in the mods index directory."""
        return list(Path(self.instance).glob("minecraft/mods/.index/*.pw.toml"))

    @property
    def mods(self) -> list[Path]:
        """Return a list of all mod files (.jar and .disabled)."""
        jar_files = list(Path(self.instance).glob("minecraft/mods/*.jar"))
        disabled_files = list(Path(self.instance).glob("minecraft/mods/*.disabled"))
        return jar_files + disabled_files

    @property
    def enabled_mods(self) -> list[Path]:
        """Return a list of enabled mods (.jar)."""
        return list(Path(self.instance).glob("minecraft/mods/*.jar"))

    @property
    def disabled_mods(self) -> list[Path]:
        """Return a list of disabled mods (.disabled)."""
        return list(Path(self.instance).glob("minecraft/mods/*.disabled"))

    @staticmethod
    def get_instances() -> list[Path]:
        """Get available PrismLauncher instances as a list of directories."""
        instances = Path(os.getenv('APPDATA'), 'PrismLauncher', 'instances')
        if not instances.exists():
            raise FileNotFoundError(f"The directory {instances} does not exist.")
        return [
            instance for instance in instances.iterdir()
            if instance.is_dir()
            and (instance / "minecraft").is_dir()
        ]

    def get_data_from_saved(self, saved, name="", path=Path()):
        for data in saved:
            if name == data["name"]:
                return data
            print(name, path, get_stem(path) + ".jar", data["filename"], sep="\n")
            if get_stem(path) + ".jar" == data["filename"]:
                return data

    def get_data(self, name="", path=Path("")):
        for data in self.local_data:
            if path:
                if data["filename"] == get_stem(path) + ".jar":
                    return self.single_data(data["path"], anyway=True)
            print(data["name"], name)
            if data["name"] == name:
                return self.single_data(data["path"], anyway=True)

