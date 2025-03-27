# PrismModOrganizer  

PrismModOrganizer is a tool designed for managing mods in **Prism Launcher**. It fetches mod data from **Modrinth** and **CurseForge**, generates `.md` files, and continuously syncs them while the program is running. It tracks any changes to mods whether they are added, enabled, disabled, or removed and automatically updates the corresponding `.md` files.  
  
## FAQ ❓

### How to work with CurseForge?

To use **CurseForge** with PrismModOrganizer, you need to provide your **API key**. Here's how to get it:

1. Visit [CurseForge API Keys](https://console.curseforge.com/#/api-keys).
2. Generate a new API key.
3. Enter this key into the program’s **CurseForge Integration** settings.

### How can I make properties in `.md` files more compact?

You can simplify the properties displayed in `.md` files by hiding unnecessary fields. To do this:

1. Open the `tags_whitelist.txt` file.
2. Add the names of the properties you want to keep visible. This will hide others, but they’ll still be searchable.

To activate this feature, follow these steps:

1. Open **Obsidian**.
2. Go to **Appearance** > **CSS snippets**.
3. Enable the snippets created by the program during its first run.

## Reporting Issues 🐞

If you encounter any bugs or have feature suggestions, please submit them on the [GitHub Issues page](#). We value your feedback!
