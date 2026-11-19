"""Refresh the "Latest writing" list in README.md from the DEV.to API."""
import json
import re
import urllib.request

USERNAME = "amananandrai"
COUNT = 5
START = "<!-- BLOG-POST-LIST:START -->"
END = "<!-- BLOG-POST-LIST:END -->"

url = f"https://dev.to/api/articles?username={USERNAME}&per_page={COUNT}"
req = urllib.request.Request(url, headers={"User-Agent": "readme-blog-updater"})
with urllib.request.urlopen(req, timeout=30) as resp:
    articles = json.load(resp)

if not articles:
    raise SystemExit("No articles returned; leaving README unchanged.")

def esc(title):
    return re.sub(r"([\[\]])", r"\\\1", title.strip())

lines = [f"- [{esc(a['title'])}]({a['url']})" for a in articles[:COUNT]]
block = f"{START}\n" + "\n".join(lines) + f"\n{END}"

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
if not pattern.search(readme):
    raise SystemExit("Markers not found in README.md")

updated = pattern.sub(lambda _: block, readme)
if updated != readme:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)
    print("README updated.")
else:
    print("No changes.")
