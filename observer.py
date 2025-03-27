from pathlib import Path
from queue import Queue

from watchdog.events import FileSystemEventHandler

from utils import stem


class ModFileHandler(FileSystemEventHandler):
    def __init__(self, task_queue: Queue):
        self.queue = task_queue

    def disable_mod(self, path: Path | str):
        self.queue.put({"action": "disable", "path": path})

    def enable_mod(self, path: Path | str):
        self.queue.put({"action": "enable", "path": path})

    def create_mod(self, path: Path | str):
        self.queue.put({"action": "create", "path": path})

    def delete_mod(self, path: Path | str):
        self.queue.put({"action": "delete", "path": path})

    @staticmethod
    def valid_suffix(event):
        return event.src_path.endswith(".jar") or event.src_path.endswith(".jar.disabled")

    def on_moved(self, event):
        if not event.is_directory and self.valid_suffix(event):
            src = Path(event.src_path)
            dest = Path(event.dest_path)
            if src.parent == dest.parent and stem(src) == stem(dest):
                if src.suffix == ".jar" and dest.suffix == ".jar.disabled":
                    self.disable_mod(src)
                elif src.suffix == ".jar.disabled" and dest.suffix == ".jar":
                    self.enable_mod(src)

    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith(".jar") or event.src_path.endswith(".jar.disabled")):
            return self.create_mod(Path(event.src_path))

    def on_deleted(self, event):
        if not event.is_directory and (event.dest_path.endswith(".jar") or event.dest_path.endswith(".jar.disabled")):
            return self.delete_mod(Path(event.src_path))