from dynaconf import Dynaconf
import json

GITHUB_USERNAME = "BlTT6956"
PROJECT_NAME = "PrismModOrganizer"
VERSION = "1.0.0"
CONTACT = "bltt6956@gmail.com"

MODRINTH_PROJECT = "https://api.modrinth.com/v2/project/{}"
MODRINTH_VERSION = "https://api.modrinth.com/v2/version/{}"
MODRINTH_USER_AGENT = "{}/{}/{} ({})"

CURSEFORGE_PROJECT = "https://api.curseforge.com/v1/mods/{}"
CURSEFORGE_VERSION = "https://api.curseforge.com/v1/mods/{}/files/{}"


default_json = {
    "INSTANCE_PATH": "",
    "OBSIDIAN_PATH": ""
}

class Settings:
    def __init__(self, file_path, default_json):
        self.file_path = file_path
        self.default_json = default_json

    def __getattr__(self, name):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            value = data.get(name)
            if isinstance(value, list) and len(value) == 1:
                return value[0]
            return value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.reset()

    def __setattr__(self, name, value):
        # Обновляем файл при изменении данных
        if name in ['file_path', 'default_json']:
            super().__setattr__(name, value)
        else:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = self.default_json

            data[name] = value

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def reset(self):
        with open(self.file_path, "w") as file:
            json.dump(self.default_json, file, indent=4, ensure_ascii=False)

settings = Settings("settings.json", default_json)