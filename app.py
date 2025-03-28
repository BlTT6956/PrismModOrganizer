import traceback
from utils import base_path
from menu import Menu

def main():
    print("Prism Mod Organizer is starting...")
    try:
        Menu.start()
    except KeyboardInterrupt:
        print("The program was completed.")
    except Exception as e:
        with open(str(base_path("crash.txt")), "w") as crash_file:
            traceback.print_exc(file=crash_file)
        print("An error has occurred. The information is recorded in crash.txt.")

if __name__ == "__main__":
    main()