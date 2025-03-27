import time
from pathlib import Path
import threading
from queue import Queue

from tqdm import tqdm
from watchdog.observers import Observer

from transformer import from_platform
from modrinth import Modrinth
from curseforge import CurseForge
from prism import Prism
from setting import settings
from obsidian import Vault, Note
from utils import suffix, stem
from observer import ModFileHandler

class Processor:
    def __init__(self):
        self.instance = Prism(settings.INSTANCE_PATH)
        self.obsidian = Vault(settings.OBSIDIAN_MAIN_PATH, settings.OBSIDIAN_MODS_PATH, settings.OBSIDIAN_ARCHIVE_PATH, settings.OBSIDIAN_TEMPLATE_PATH)
        self.template = self.get_content(settings.OBSIDIAN_TEMPLATE_PATH)

    @staticmethod
    def get_content(path: Path | str):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def basic_enabled(self, basic: dict) -> bool:
        return basic["Stem"] in self.instance.enabled_stems

    def load_basic(self, path: Path | str) -> dict:
        return from_platform(self.load_local(path))

    def load_local(self, path: Path | str) -> dict:
        if suffix(path) == ".pw.toml":
            return self.instance.get_local_toml(path)
        else:
            return self.instance.get_local_stem(path)

    def load_full(self, path: Path | str) -> dict:
        local = self.load_local(path)
        basic = self.load_basic(local["filename"])
        enabled = self.basic_enabled(basic)
        project = {}
        version = {}
        dependencies = []
        if basic["Platform"] == "modrinth":
            project = Modrinth.get_project(basic["Project ID"])
            version = Modrinth.get_version(basic["Version ID"])
            dependencies = Modrinth.get_dependencies(version)
        elif basic["Platform"] == "curseforge":
            project = CurseForge.get_project(basic["Project ID"])
            version = CurseForge.get_version(basic["Project ID"], basic["Version ID"])
            dependencies = CurseForge.get_dependencies(version)
        return from_platform(local, enabled, project, version, dependencies)

    def startup_mods(self) -> list[Note]:
        result = []
        mods, archive = self.obsidian.mods_dict, self.obsidian.archive_dict
        for toml in tqdm(self.instance.toml, desc="Loading mods..."):
            self.create_mod(toml, mods, archive)
        return result

    def create_mod(self, path: Path | str, mods=None, archive=None) -> Note:
        data = self.load_basic(path)
        mods = mods or self.obsidian.mods_dict
        archive = archive or self.obsidian.archive_dict
        mod = mods.get(data["Stem"]) or archive.get(data["Stem"])
        if mod:
            mod = mod.recover()
            if data["File update"] != mod.get("File update"):
                data = self.load_full(path)
                mod.metadata = data
        else:
            data = self.load_full(path)
            return self.obsidian.create_note(data["Name"], metadata=data, content=self.template)

    def enable_mod(self, path: Path | str) -> Note:
        data = stem(path)
        return self.obsidian.find_mod("Stem", data).enable()

    def disable_mod(self, path: Path | str) -> Note:
        data = stem(path)
        return self.obsidian.find_mod("Stem", data).disable()

    def delete_mod(self, path: Path | str) -> Note:
        data = stem(path)
        return self.obsidian.find_mod("Stem", data).archive()

    def process_tasks(self, task_queue: Queue):
        while True:
            task = task_queue.get()
            if task is None:
                break
            else:
                match task["action"]:
                    case "disable":
                        self.disable_mod(task["path"])
                    case "enable":
                        self.enable_mod(task["path"])
                    case "create":
                        self.create_mod(task["path"])
                    case "delete":
                        self.delete_mod(task["path"])
            task_queue.task_done()

    def run(self):
        observer = Observer()
        event_handler = ModFileHandler(Queue())
        observer.schedule(event_handler, self.instance.instance / "minecraft" / "mods", recursive=False)
        observer.start()

        worker_thread = threading.Thread(target=self.process_tasks, args=(event_handler.queue,), daemon=True)
        worker_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            event_handler.queue.put(None)
        observer.join()
        worker_thread.join()