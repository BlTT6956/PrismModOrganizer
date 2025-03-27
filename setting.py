import json
from pathlib import Path


default_json = {
    "INSTANCE_PATH": "",
    "OBSIDIAN_MODS_PATH": "",
    "OBSIDIAN_ARCHIVE_PATH": "",
    "OBSIDIAN_TEMPLATE_PATH": "",
    "OBSIDIAN_MAIN_PATH": ""
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