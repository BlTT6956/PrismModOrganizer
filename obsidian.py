from pathlib import Path
from template import template

class Obsidian:
    def __init__(self, path):
        self.path = Path(path)

    def create_md(self, data, replace=False):
        if replace or not self.check_md(data):
            with open(self.path / f"{data["name"]}.md", "w") as f:
                f.write(template(data))

    def check_md(self, data):
        return (self.path / f"{data["name"]}.md").is_file()