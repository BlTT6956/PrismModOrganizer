import json
from pathlib import Path

from utils import base_path

default_json = {
    "INSTANCE_PATH": "",
    "OBSIDIAN_MODS_PATH": "",
    "OBSIDIAN_ARCHIVE_PATH": "",
    "OBSIDIAN_TEMPLATE_PATH": "",
    "OBSIDIAN_MAIN_PATH": ""
}

settings_path = base_path("settings.json")

class Settings:
    def __init__(self, file_path, default_json):
        self.file_path = Path(file_path)
        self.default_json = default_json
        self.file_path.touch(exist_ok=True)  # Создаем файл, если его нет
        self._ensure_json_exists()

    def _ensure_json_exists(self):
        """Создает файл с настройками, если он пуст или поврежден."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.reset()

    def reset(self):
        """Сбрасывает файл настроек до значений по умолчанию."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.default_json, file, indent=4, ensure_ascii=False)

    def __getattr__(self, name):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get(name)

    def __setattr__(self, name, value):
        if name in ['file_path', 'default_json']:
            super().__setattr__(name, value)
        else:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data[name] = value
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

settings = Settings(settings_path, default_json)