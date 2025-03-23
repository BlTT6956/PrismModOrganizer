import os
import shutil
from pathlib import Path
import threading
from template import template
from setting import settings


class Obsidian:
    def __init__(self, path):
        self.path = Path(path)
        self.prism = None
        self.mod_folder = self.path / Path(settings.OBSIDIAN_MODS_FOLDER)
        self.mod_folder.mkdir(parents=True, exist_ok=True)
        self.deleted_folder = self.path / Path(settings.OBSIDIAN_DELETED_FOLDER)
        self.deleted_folder.mkdir(parents=True, exist_ok=True)

    @property
    def mods(self):
        return self.mod_folder.glob("*.md")

    def create_mod(self, param, saved=None):
        thread = threading.Thread(target=self._create_mod, args=(param, saved))
        thread.start()

    def _create_mod(self, param, saved=None):
        if isinstance(param, dict):
            data = param
        else:
            if saved:
                data = self.prism.get_data_from_saved(path=param, saved=saved)
            else:
                data = self.prism.get_data(path=param)
        file_name = f"{data['name']}.md"
        file_path = self.mod_folder / file_name
        deleted_file_path = self.deleted_folder / file_name

        if deleted_file_path.exists():
            shutil.move(deleted_file_path, file_path)
            self.update_mod(data, saved)
        else:
            if not self.check_md(data):
                with open(file_path, "w") as f:
                    f.write(template(data))
            else:
                self.update_mod(data, saved)

    def check_md(self, param, saved=None):
        if isinstance(param, dict):
            data = param
        else:
            if saved:
                data = self.prism.get_data_from_saved(path=param, saved=saved)
            else:
                data = self.prism.get_data(path=param)
        return (self.mod_folder / f"{data['name']}.md").is_file()

    def turn_mod_state(self, param, saved=None, mode=None):
        thread = threading.Thread(target=self._turn_mod_state, args=(param, saved, mode))
        thread.start()

    def _turn_mod_state(self, param, saved=None, mode=None):
        if isinstance(param, dict):
            data = param
        else:
            if saved:
                data = self.prism.get_data_from_saved(path=param, saved=saved)
            else:
                data = self.prism.get_data(path=param)
        if not (mode is None):
            data["enabled"] = mode
        with open(self.mod_folder / f"{data['name']}.md", "r+") as f:
            print("Turning", data["name"])
            text = f.read()
            if "Enabled: True" in text:
                text = text.replace("Enabled: True", f"Enabled: {data["enabled"]}", 1)
            elif "Enabled: False" in text:
                text = text.replace("Enabled: False", f"Enabled: {data["enabled"]}", 1)
            f.seek(0)
            f.write(text)
            f.truncate()

    def update_mod(self, param, saved=None):
        thread = threading.Thread(target=self._update_mod, args=(param, saved))
        thread.start()

    def _update_mod(self, param, saved=None):
        if isinstance(param, dict):
            data = param
        else:
            if saved:
                data = self.prism.get_data_from_saved(path=param, saved=saved)
            else:
                data = self.prism.get_data(path=param)
        with open(self.mod_folder / f"{data['name']}.md", "r+") as f:
            text = f.read()
            human_text = text.split("---")[-1]
            f.seek(0)
            f.truncate(0)
            f.write(template(data) + "  " + human_text)

    def delete_mod(self, param, saved=None):
        thread = threading.Thread(target=self._turn_mod_state, args=(param, saved, False))
        thread.start()
        thread = threading.Thread(target=self._delete_mod, args=(param, saved))
        thread.start()

    def delete_md(self, name):
        if not self.deleted_folder.exists():
            os.makedirs(self.deleted_folder)
        file_path = self.mod_folder / f"{name}.md"
        if file_path.exists():
            shutil.move(file_path, self.deleted_folder / f"{name}.md")

    def _delete_mod(self, param, saved=None):
        if isinstance(param, dict):
            data = param
        else:
            if saved:
                data = self.prism.get_data_from_saved(path=param, saved=saved)
            else:
                data = self.prism.get_data(path=param)
        if not self.deleted_folder.exists():
            os.makedirs(self.deleted_folder)
        file_path = self.mod_folder / f"{data['name']}.md"

        if file_path.exists():
            shutil.move(file_path, self.deleted_folder / f"{data['name']}.md")
