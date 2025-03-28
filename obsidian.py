from pathlib import Path
import yaml
import shutil
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter as tk
from utils import read_whitelist
import re

from setting import settings

class Vault:
    def __init__(self, main_path: Path | str, mods_path: Path | str, archive_path: Path | str, template_path: Path | str):
        self.main_folder = Path(main_path)
        self.main_folder.mkdir(parents=True, exist_ok=True)
        self.mods_folder = Path(mods_path)
        self.mods_folder.mkdir(parents=True, exist_ok=True)
        self.archive_folder = Path(archive_path)
        self.archive_folder.mkdir(parents=True, exist_ok=True)
        self.template_path = Path(template_path)
        self.template_path.parent.mkdir(parents=True, exist_ok=True)
        self.snippets_folder = (self.main_folder / ".obsidian" / "snippets")
        self.snippets_folder.mkdir(parents=True, exist_ok=True)

        if not self.template_path.exists():
            self.template_path.touch()

        self.whitelist = read_whitelist()
        self.whitelist_snippet()
        self.hide_prop_add_button_snippet()

        self.cached_mods = None
        self.cached_archive = None

    def _load_mods(self):
        self.cached_mods = [Note(self, path) for path in self.mod_files]

    def _load_archive(self):
        self.cached_archive = [Note(self, path) for path in self.archive_files]

    @staticmethod
    def reset_template():
        if not settings.OBSIDIAN_TEMPLATE_PATH:
            Vault.select_obsidian_template()
            Vault.reset_template()
        else:
            Path(settings.OBSIDIAN_TEMPLATE_PATH).parent.mkdir(parents=True, exist_ok=True)
            with open(settings.OBSIDIAN_TEMPLATE_PATH, "w") as file:
                file.write("---\n\n")
                file.write("`= \"![|150](\" + this.icon + \")\"`\n\n")
                file.write("`= this.description`")

    def hide_prop_add_button_snippet(self):
        snippets_file = self.snippets_folder / "PMO-HidePropAddButton.css"
        if not snippets_file.exists():
            snippets_file.touch()
        with open(snippets_file, 'w') as f:
            #f.write(".markdown-preview-view\n")
            f.write(".metadata-add-button {\n")
            f.write("  display: none;\n")
            f.write("}\n")

    def whitelist_snippet(self):
        snippets_file = self.snippets_folder / "PMO-Whitelist.css"
        if not snippets_file.exists():
            snippets_file.touch()
        with open(snippets_file, 'w') as f:
            f.write("div.metadata-properties > div.metadata-property {\n")
            f.write("  display: none !important;\n")
            f.write("}\n\n")

            for prop in self.whitelist:
                f.write(f"div.metadata-properties > div.metadata-property[data-property-key=\"{prop}\"] {{\n")
                f.write("  display: flex !important;\n")
                f.write("}\n")

    @staticmethod
    def select_obsidian_folder(title: str = ""):
        root = tk.Tk()
        root.withdraw()
        root.lift()
        root.focus_force()
        return askdirectory(parent=root, title=title)

    @staticmethod
    def select_obsidian_path(title: str = ""):
        root = tk.Tk()
        root.withdraw()
        root.lift()
        root.focus_force()
        return askopenfilename(parent=root, title=title, filetypes=[("Markdown Files", "*.md")])

    @staticmethod
    def select_obsidian_vault_folder():
        print("Select the main Obsidian Vault folder...")
        instance = Vault.select_obsidian_folder("Select the main Obsidian Vault folder...")
        settings.OBSIDIAN_MAIN_PATH = str(instance)

    @staticmethod
    def select_obsidian_mods_folder():
        print("Select the Obsidian mods folder...")
        instance = Vault.select_obsidian_folder("Select the Obsidian mods folder...")
        settings.OBSIDIAN_MODS_PATH = str(instance)

    @staticmethod
    def select_obsidian_archive_folder():
        print("Select the Obsidian archive folder...")
        instance = Vault.select_obsidian_folder("Select the Obsidian archive folder...")
        settings.OBSIDIAN_ARCHIVE_PATH = str(instance)

    @staticmethod
    def select_obsidian_template():
        while True:
            print("1) Generate a standard template file in your Obsidian Vault folder")
            print("2) Select template file")
            answer = input("~ ")
            match answer:
                case "1":
                    settings.OBSIDIAN_TEMPLATE_PATH = str(Path(settings.OBSIDIAN_MAIN_PATH) / "template.md")
                    Vault.reset_template()
                    return
                case "2":
                    instance = Vault.select_obsidian_path("Select a template for mods in Obsidian...")
                    settings.OBSIDIAN_TEMPLATE_PATH = str(instance)
                    return

    def find_mod(self, key, value):
        return next((mod for mod in self.mods if mod.get(key) == value), None)

    def find_mods(self, key, value):
        return [mod for mod in self.mods if mod.get(key) == value]

    def find_archive(self, key, value):
        return next((mod for mod in self.archive if mod.get(key) == value), None)

    def find_archives(self, key, value):
        return [mod for mod in self.archive if mod.get(key) == value]

    @property
    def archive_files(self):
        return list(self.archive_folder.glob("*.md"))

    @property
    def mod_files(self):
        return list(self.mods_folder.glob("*.md"))

    @property
    def archive(self):
        if self.cached_archive is None:
            self._load_archive()
        return self.cached_archive

    @property
    def mods(self):
        if self.cached_mods is None:
            self._load_mods()
        return self.cached_mods

    @property
    def archive_dict(self):
        return {note.get("Stem"): note for note in self.archive}

    @property
    def mods_dict(self):
        return {note.get("Stem"): note for note in self.mods}

    def create_note(self, name: str, content: str = None, metadata: dict = None, to_archive=False):
        note_name = f"{name}.md"
        note_path = self.archive_folder / note_name if to_archive else self.mods_folder / note_name

        with open(note_path, 'w', encoding='utf-8') as file:
            if content:
                file.write(content)

        note = Note(self, note_path)
        if metadata:
            note.metadata = metadata

        if to_archive:
            if self.cached_archive is not None:
                self.cached_archive.append(note)
        else:
            if self.cached_mods is not None:
                self.cached_mods.append(note)

        return note


class Note:
    def __init__(self, vault: Vault, path: Path):
        self.vault = vault
        self.path = path
        self._cached_content = None
        self._cached_metadata = None

    @property
    def content(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            return file.read()

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be string.")
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(value)

    @property
    def metadata(self):
        if self._cached_metadata is None:
            self._cached_metadata = self._load_metadata()
        return self._cached_metadata

    @metadata.setter
    def metadata(self, value):
        if not isinstance(value, dict):
            raise ValueError("Metadata must be a dictionary.")
        self._cached_metadata = value  # Обновляем кэш
        self._save_metadata(value)

    def has_metadata(self):
        return bool(re.match(r"^---\n(.*?)\n---\n", self.content, re.DOTALL))

    def extract_metadata(self):
        match = re.match(r"^---\n(.*?)\n---\n", self.content, re.DOTALL)
        if not match:
            return {}

        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}

    def extract_content(self):
        return re.sub(r"^---\n.*?\n---\n", "", self.content, flags=re.DOTALL).lstrip()

    def get(self, key):
        return self.metadata.get(key, None)

    def set(self, key, value):
        new_metadata = self.metadata
        new_metadata[key] = value
        self._save_metadata(new_metadata)
        return self

    def _load_metadata(self):
        if self.has_metadata():
            return self.extract_metadata()
        return {}

    def _save_metadata(self, metadata=None):
        if metadata is None:
            metadata = self.metadata

        new_metadata = yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip()

        if self.has_metadata():
            content_without_metadata = self.extract_content()
        else:
            content_without_metadata = self.content

        new_content = f"---\n{new_metadata}\n---\n{content_without_metadata}"
        self._cached_content = new_content
        self._cached_metadata = metadata

        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(new_content)

    @property
    def archived(self):
        return self.path in self.vault.archive_files

    def archive(self):
        destination = self.vault.archive_folder / self.path.name
        if destination not in self.vault.archive_files:
            self.vault.archive_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(self.path), destination)
            self.path = destination
            self.vault.cached_archive.append(self)
            self.vault.cached_mods.remove(self)
        return self

    def recover(self):
        destination = self.vault.mods_folder / self.path.name
        if not destination.exists():
            self.vault.mods_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(self.path), destination)
            self.path = destination
            self.vault.cached_mods.append(self)
            self.vault.cached_archive.remove(self)
        return self

    @property
    def enabled(self):
        return bool(self.get("Enabled"))

    def enable(self):
        self.set("Enabled", True)
        return self

    def disable(self):
        self.set("Enabled", False)
        return self

    def toggle(self, state=None):
        if state is not None:
            self.enable() if state else self.disable()
            return self
        else:
            self.disable() if self.enabled else self.enable()
            return self
