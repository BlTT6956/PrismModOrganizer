from utils import format_number
from converter import curseforge_to_modrinth


def template(data):
    return f"""---
Name: {data["name"]}
Filename: {data["filename"]}
Enabled: {data["enabled"]}
Side: {data['side']}
{"Client side: " + data['project']['client_side'] + '\n' if data["project"]["client_side"] != "None" else ""}
{"Server side: " + data['project']['server_side'] + '\n' if data["project"]["server_side"] != "None" else ""}
{"Dependencies:\n" + "\n".join([f'- "[[{dep}]]"' for dep in data['dependencies']]) + '\n' if data["dependencies"] else ""}
---
---
{f'''
<div style="display: flex; align-items: flex-start; height: 100%;">
  <img src="{data['project']['icon_url']}" style="align-self: stretch; width: 120px; height: 120px;">
  <div style="display: flex; flex-direction: column; justify-content: flex-start; height: 100%; flex-grow: 1; margin-left: 20px;">
    <p style="margin: 0; padding: 0;">{data['project']['description']}</p>
    <div style="display: flex; align-items: center; margin-top: auto;">
      <div style="display: flex; align-items: center; margin-right: 20px;">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" class="h-6 w-6 text-secondary" width="24" height="24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3v-1m-4-4-4 4m0 0-4-4m4 4V4"></path>
        </svg>
        <p style="margin-left: 3px; font-weight: bold;">{format_number(data['project']['downloads'])}</p>
      </div>
      {f'''
      <div style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="h-6 w-6 text-secondary" width="24" height="24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 0 0 0 6.364L12 20.364l7.682-7.682a4.5 4.5 0 0 0-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 0 0-6.364 0"></path>
        </svg>
        <p style="margin-left: 3px; font-weight: bold;">{format_number(data['project']['followers'])}</p>
      </div>
      ''' if format_number(data['project']['followers']) != "0" else ''}
    </div>
  </div>
</div>
'''}
{" ".join(sorted(list(dict.fromkeys([f"#{curseforge_to_modrinth(i)}".lower() for i in data["project"]["categories"]]))))}
#{data["side"]}
"""