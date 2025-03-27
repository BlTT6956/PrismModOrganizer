import platform, os, re
import keyring
from pathlib import Path

def clear_console():
    """
    Clears the terminal/console based on the OS (Windows or Unix-like).
    """
    system = platform.system().lower()
    if system == 'windows':
        os.system('cls')
    else:
        os.system('clear')


def sanitize_filename(filename, os_type='windows'):
    """Removes forbidden characters from a filename."""
    forbidden_chars = r'[<>:"/\\|?*\[\]]'
    sanitized_filename = re.sub(forbidden_chars, '', filename)
    return sanitized_filename


def format_number(num: int) -> str:
    """
    Formats a number with 'k' for thousands and 'M' for millions.
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}k"
    else:
        return str(num)


def format_list(lst: list) -> list:
    """
    Formats each element in the list with double square brackets.
    """
    return [f"[[{elem}]]" for elem in lst]

def read_whitelist():
    default = ["enable", "game_versions"]

    if Path("tags_whitelist.txt").exists():
        with open("tags_whitelist.txt", "r") as file:
            return file.read().split("\n")
    else:
        with open("tags_whitelist.txt", "w") as file:
            file.writelines(default)
            return default

def save_api_key():
    """Asks the user for an API key and stores it in the OS keyring."""
    api_key = input("Enter CurseForge API key: ")
    keyring.set_password("PrismObsidian", "PrismObsidian", api_key)
    return api_key

def get_api_key() -> str:
    """Retrieves the API key from the OS keyring."""
    return keyring.get_password("PrismObsidian", "PrismObsidian") or save_api_key()

def stem(path: Path | str) -> str:
    return re.sub(r'(\.jar|\.jar\.disabled|\.pw\.toml|\.md)$', '', str(path.name))

def suffix(path: Path | str) -> str:
    match = re.search(r'(\.jar\.disabled|\.jar|\.pw\.toml|\.md)$', str(path))
    return match.group(1) if match else ''