from pathlib import Path
import toml
import os
import datetime

from utils import stem

class Prism:
    def __init__(self, instance: Path | str):
        self.instance = Path(instance)

    @property
    def toml(self) -> list[Path]:
        """Return a list of .pw.toml files in the mods index directory."""
        return list(Path(self.instance).glob("minecraft/mods/.index/*.pw.toml"))

    @property
    def enabled_mods(self) -> list[Path]:
        """Return a list of enabled mods (.jar)."""
        return list(Path(self.instance).glob("minecraft/mods/*.jar"))

    @property
    def enabled_stems(self) -> list[str]:
        return [stem(path) for path in self.enabled_mods]

    @property
    def disabled_mods(self) -> list[Path]:
        """Return a list of disabled mods (.disabled)."""
        return list(Path(self.instance).glob("minecraft/mods/*.disabled"))

    @property
    def disabled_stems(self) -> list[str]:
        return [stem(path) for path in self.disabled_mods]

    @property
    def mods(self) -> list[Path]:
        """Return a list of all mod files (.jar and .disabled)."""
        return self.enabled_mods + self.disabled_mods

    def get_local_toml(self, toml_file: str | Path) -> dict:
        data = toml.loads((self.instance / "minecraft/mods/.index" / str(toml_file)).read_text(encoding="utf-8"))
        data["Date"] = datetime.datetime.fromtimestamp(toml_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        return data

    def get_local_slug(self, slug: str | Path) -> dict:
        return self.get_local_toml(slug / ".pw.toml")

    def get_local_stem(self, stem_name: str | Path) -> dict:
        return self.get_local_key_value("filename", f"{stem(Path(stem_name))}.jar")

    def get_local_key_value(self, key: str, value) -> dict:
        for toml_file in self.toml:
            toml_text = self.get_local_toml(toml_file)
            if toml_text.get(key, {}) == value:
                toml_text["Date"] = datetime.datetime.fromtimestamp(toml_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                return toml_text

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