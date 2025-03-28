# PrismModOrganizer  

PrismModOrganizer is a tool designed for managing mods in [Prism Launcher](https://prismlauncher.org/) with seamless integration into [Obsidian](https://obsidian.md/). It fetches mod data from (Modrinth)[https://modrinth.com/] and (CurseForge)[https://www.curseforge.com/], automatically generates `.md` files, and keeps them continuously synced while running. The program tracks any changes to mods—whether they are added, enabled, disabled, or removed—and updates the corresponding `.md` files in your Obsidian vault.  

## ❓ FAQ  

### How to use CurseForge?  

To integrate CurseForge with PrismModOrganizer, you need to provide an API key:  

1. Visit the [CurseForge API Keys](https://www.curseforge.com) page.  
2. Generate a new API key.  
3. Enter this key in the program’s CurseForge integration settings.  

### How can I make properties in `.md` files more compact?  

You can simplify the displayed properties in `.md` files by hiding unnecessary fields:  

1. Open the `tags_whitelist.txt` file.  
2. Add the names of the properties you want to keep visible. Others will be hidden but will remain searchable.  

To activate this feature:  

1. Open **Obsidian**.  
2. Go to **Settings > Appearance > CSS Snippets**.  
3. Enable the CSS snippets created by the program during its first run.  

## 🐞 Reporting Issues  

If you encounter any bugs or have feature suggestions, please submit them on [GitHub Issues](#). Your feedback helps improve PrismModOrganizer!  
