import time
from watchdog.events import FileSystemEventHandler
import threading
import re

import utils
from utils import get_stem, get_suffix, path_without_suffix
from pathlib import Path


class EventManager:
    def __init__(self, instance, obsidian):
        self.instance = instance
        self.obsidian = obsidian
        self.events = []
        self.events_lock = threading.Lock()
        self.saved_toml = self.instance.local_data
        self.saved_mods = self.instance.mods
        self.old_saved_mods = self.instance.mods
        self.forget_next_rename = 0

    def tick(self):
        while True:
            flag = False
            with self.events_lock:
                for event in filter(lambda e: e.event_type == "deleted" and Path(e.src_path).parent.name == "mods", self.events):
                    path = Path(event.src_path)
                    if time.time() - event.event_time >= 2:
                        self.obsidian.delete_mod(path, self.saved_toml)
                        self.events.remove(event)
                        flag = True
                        self.old_saved_mods.remove(path)
                        for sub_event in filter(lambda e: e.event_type == "deleted" and get_stem(Path(e.src_path)) == get_stem(data["path"]), self.events):
                            self.events.remove(sub_event)
                        continue
                if flag:
                    self.saved_toml = self.instance.local_data
                for event in filter(lambda e: e.event_type == "created" and Path(e.src_path).parent.name == "mods", self.events):
                    path = Path(re.sub(r'(\.jar|\.jar\.disabled)\..*', r'\1', event.src_path))
                    if path.suffix in (".disabled", ".jar") and time.time() - event.event_time >= 2:
                        data = self.instance.get_data(Path(path=utils.get_stem(path)))
                        self.obsidian.create_mod(data)
                        self.events.remove(event)
                        self.old_saved_mods.append(path)
                        for sub_event in filter(lambda e: e.event_type == "created" and get_stem(Path(e.src_path)) == get_stem(data["path"]), self.events):
                            self.events.remove(sub_event)
                for event in filter(lambda e: e.event_type == "edited" and Path(e.src_path).name == ".index", self.events):
                    path = Path(event.src_path)
                    if event.src_path.endswith(".pw.toml"):
                        self.obsidian.update_mod(path)
                        self.events.remove(event)
            self.saved_mods = self.instance.mods
            if self.saved_mods != self.old_saved_mods:
                for path in self.saved_mods:
                    if path.suffix == ".jar" and Path(str(path_without_suffix(path)) + ".jar.disabled") in self.old_saved_mods:
                        data = self.instance.get_data_from_saved(path=path, saved=self.instance.local_data)
                        data["enabled"] = True
                        self.obsidian.turn_mod_state(data)
                        self.old_saved_mods.remove(path.with_suffix(".jar.disabled"))
                        self.old_saved_mods.append(path)
                    elif path.suffix == ".disabled":
                        old_path = Path(path.parent, path.stem)
                        if old_path in self.old_saved_mods:
                            data = self.instance.get_data_from_saved(path=path, saved=self.instance.local_data)
                            data["enabled"] = False
                            self.obsidian.turn_mod_state(data)
                            self.old_saved_mods.remove(old_path)
                            self.old_saved_mods.append(path)
            # if self.obsidian.state_processing == 0:
            #     for md in self.obsidian.mods:
            #         with open(md, "r") as f:
            #             text = f.read()
            #             value = True if re.search(r'Enabled: (true|false)', text, re.IGNORECASE).group(1) == "true" else False
            #             filename = Path(re.search(r'Filename:\s*([^\s]+\.jar)', text).group(1)).stem
            #             for file in self.instance.mods:
            #                 if get_stem(file) == filename:
            #                     if get_suffix(file) == ".jpg" and not value:
            #                         file.rename(Path(str(path_without_suffix(file)) + ".disabled"))
            #                         self.forget_next_rename += 1
            #                     elif get_suffix(file) == ".jpg.disabled" and value:
            #                         file.rename(Path(str(path_without_suffix(file)) + ".jpg"))
            #                         self.forget_next_rename += 1
            time.sleep(0.0001)


    def start_ticks(self):
        tick_thread = threading.Thread(target=self.tick)
        tick_thread.daemon = True
        tick_thread.start()


class ModEventsHandler(FileSystemEventHandler):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def on_deleted(self, event):
        if not event.is_directory:
            print("on_deleted")
            event.event_time = time.time()
            with self.event_manager.events_lock:
                self.event_manager.events.append(event)

    def on_created(self, event):
        if not event.is_directory:
            print("on_created")
            event.event_time = time.time()
            with self.event_manager.events_lock:
                self.event_manager.events.append(event)

    def on_edited(self, event):
        if not event.is_directory:
            print("on_edited")
            event.event_time = time.time()
            with self.event_manager.events_lock:
                self.event_manager.events.append(event)