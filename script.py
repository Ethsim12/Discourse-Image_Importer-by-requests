import json
import random
from zipfile import ZIP_DEFLATED
import zipfile
import unicodedata
import re
from html.parser import HTMLParser
from urllib.parse import urlparse
import requests


# --- paste your JSON between the triple quotes ---
with open("<<<<<JSON filename>>>>>.json", "r", encoding="utf-8") as f:
    json_text = f.read()
# -------------------------------------------------


class LightboxImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self._current_lightbox = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "a" and "lightbox" in attrs_dict.get("class", ""):
            self._current_lightbox = {
                "href": attrs_dict.get("href"),
            }

        elif tag == "img" and self._current_lightbox is not None:
            alt = attrs_dict.get("alt", "").strip()
            base62 = attrs_dict.get("data-base62-sha1")
            width = attrs_dict.get("width")
            height = attrs_dict.get("height")
            href = self._current_lightbox.get("href")

            if base62 and width and height and href:
                self.images.append({
                    "alt": alt,
                    "base62": base62,
                    "width": width,
                    "height": height,
                    "href": href,
                })

    def handle_endtag(self, tag):
        if tag == "a":
            self._current_lightbox = None


def sanitise_for_path(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.strip()
    text = text.replace("/", "-").replace("\\", "-")
    return re.sub(r"\s+", " ", text) or "no_alt"


def extension_from_url(url):
    path = urlparse(url).path
    if "." in path:
        return "." + path.rsplit(".", 1)[-1].lower()
    return ".bin"


def build_zip_from_text(json_text):
    data = json.loads(json_text)
    posts = data.get("post_stream", {}).get("posts", [])

    parser = LightboxImageParser()
    for p in posts:
        cooked = p.get("cooked", "")
        parser.feed(cooked)

    images = parser.images
    if not images:
        print("No images found.")
        return

    zip_name = f"images_{random.randint(100, 999)}.zip"
    print(f"Creating: {zip_name}")

    session = requests.Session()

    with zipfile.ZipFile(zip_name, "w", ZIP_DEFLATED) as zf:
        for img in images:
            url = img["href"]
            try:
                resp = session.get(url, timeout=20)
                resp.raise_for_status()
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue

            ext = extension_from_url(url)
            safe_alt = sanitise_for_path(img["alt"])
            zip_path = f"{safe_alt}/{img['width']}/{img['height']}/{img['base62']}{ext}"

            print(f"Adding {zip_path}")
            zf.writestr(zip_path, resp.content)

    print(f"\nDONE — Saved ZIP as {zip_name} in script folder.")


# ---- RUN AUTOMATICALLY IN SPYDER ----
build_zip_from_text(json_text)
