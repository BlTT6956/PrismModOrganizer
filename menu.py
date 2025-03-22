import sys
from pathlib import Path
from obsidian import Obsidian
from utils import clear_console, save_api_key, get_api_key
from prism import Prism
from setting import settings
from tkinter.filedialog import askdirectory
from tqdm import tqdm


class Menu:
    @classmethod
    def start(cls):
        while True:
            print("1) Start")
            print("2) Select instance folder")
            print("3) Select Obsidian folder")
            print("4) Insert CurseForge API")
            print("5) Quit")
            answer = input("~ ")
            match answer:
                case "1":
                    if not settings.INSTANCE_PATH:
                        instance = cls.select_instance()
                        settings.INSTANCE_PATH = str(instance)
                    if not settings.OBSIDIAN_PATH:
                        instance = cls.select_obsidian_path()
                        settings.OBSIDIAN_PATH = str(instance)
                    if not get_api_key():
                        save_api_key()
                    obsidian = Obsidian(settings.OBSIDIAN_PATH)
                    prism = Prism(settings.INSTANCE_PATH, obsidian)

                    for path in tqdm(prism.toml, desc="Loading..."):
                        if res := prism.single_data(path):
                            obsidian.create_md(res)
                    break
                case "2":
                    instance = cls.select_instance()
                    settings.INSTANCE_PATH = str(instance)
                case "3":
                    instance = cls.select_obsidian_path()
                    settings.OBSIDIAN_PATH = str(instance)
                case "4":
                    save_api_key()
                case "5":
                    cls.quit()
                case _:
                    clear_console()



    @classmethod
    def select_instance(cls) -> Path:
        """Prompt the user to select a PrismLauncher instance and return the selected path."""
        instances_raw = Prism.get_instances()
        while True:
            for index, instance in enumerate(instances_raw, start=1):
                print(f"{index}) {instance.name}")
            answer = input("~ ")
            for index, instance in enumerate(instances_raw, start=1):
                if answer == str(index):
                    return instance
            clear_console()

    @classmethod
    def select_obsidian_path(cls):
        return Path(askdirectory())

    @classmethod
    def quit(cls):
        sys.exit()