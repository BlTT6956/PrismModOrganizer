import sys
from pathlib import Path
import os

from utils import clear_console, save_api_key, get_api_key, read_whitelist, base_path
from prism import Prism
from setting import settings
from obsidian import Vault
from processor import Processor


class Menu:
    @staticmethod
    def open_txt(file_path):
        if sys.platform == "win32":
            os.startfile(file_path)  # Windows
        elif sys.platform == "darwin":
            os.system(f"open {file_path}")  # macOS
        else:
            os.system(f"xdg-open {file_path}")  # Linux

    @classmethod
    def start(cls):
        while True:
            clear_console()
            print("\nPrism Mod Organizer\n")
            print("1) Start")
            print("2) Config")
            print("3) Quit")
            answer = input("~ ")
            match answer:
                case "1":
                    clear_console()
                    if not settings.INSTANCE_PATH:
                        instance = cls.select_instance()
                        settings.INSTANCE_PATH = str(instance)
                        clear_console()
                    if not settings.OBSIDIAN_MAIN_PATH:
                        Vault.select_obsidian_vault_folder()
                    if not settings.OBSIDIAN_MODS_PATH:
                        Vault.select_obsidian_mods_folder()
                    if not settings.OBSIDIAN_ARCHIVE_PATH:
                        Vault.select_obsidian_archive_folder()
                    if not settings.OBSIDIAN_TEMPLATE_PATH:
                        Vault.select_obsidian_template()
                    if not get_api_key():
                        save_api_key()
                    clear_console()

                    process = Processor()
                    process.startup_mods()
                    clear_console()
                    print("The program is running.")
                    print("Synchronization between Prism and Obsidian is in progress...")
                    print("Press Ctrl + C to stop.")
                    process.run()


                case "2":
                    while True:
                        clear_console()
                        print("\nPrism Mod Organizer ~ Config\n")
                        print("1) Back")
                        print("2) Set CurseForge API")
                        print("3) Paths config")
                        print("4) Open properties whitelist")
                        print("5) Reset Obsidian mod template file")
                        answer = input("~ ")
                        match answer:
                            case "1":
                                break
                            case "2":
                                save_api_key()
                            case "3":
                                while True:
                                    clear_console()
                                    print("\nPrism Mod Organizer ~ Config ~ Paths Config\n")
                                    print("1) Back")
                                    print("2) Select instance folder")
                                    print("4) Select main Obsidian Vault folder")
                                    print("4) Select Obsidian mods folder")
                                    print("5) Select Obsidian archive folder")
                                    print("6) Select a template for mods in Obsidian")
                                    answer = input("~ ")

                                    match answer:
                                        case "1":
                                            break
                                        case "2":
                                            instance = cls.select_instance()
                                            settings.INSTANCE_PATH = str(instance)
                                        case "3":
                                            Vault.select_obsidian_vault_folder()
                                        case "4":
                                            Vault.select_obsidian_mods_folder()
                                        case "5":
                                            Vault.select_obsidian_archive_folder()
                                        case "6":
                                            Vault.select_obsidian_template()
                            case "4":
                                read_whitelist()
                                Menu.open_txt(base_path("tags_whitelist.txt"))
                            case "5":
                                Vault.reset_template()
                case "3":
                    cls.quit()


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
    def quit(cls):
        sys.exit()