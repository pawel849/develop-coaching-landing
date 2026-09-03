from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []
        self.links = []
        self.images = []
        self.h1 = 0
        self.main = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "main": self.main += 1

a = Audit(); a.feed(HTML)
assert a.h1 == 1, f"Expected one h1, got {a.h1}"
assert a.main == 1, f"Expected one main, got {a.main}"
assert len(a.ids) == len(set(a.ids)), "Duplicate IDs"
assert 'lang="en"' in HTML, "Missing page language"
assert "this isn’t just a shortcut" not in HTML.lower(), "Removed sentence returned"
assert "whatsapp" not in HTML.lower(), "WhatsApp should not be present"
assert "Book a Call" in HTML, "Primary CTA missing"
assert 'id="booking"' in HTML, "Booking target missing"
assert "Calendar integration placeholder" in HTML, "Calendar placeholder missing"
assert "@media (max-width:680px)" in CSS, "Mobile CSS missing"
assert "prefers-reduced-motion" in CSS, "Reduced-motion handling missing"

ids = set(a.ids)
for link in a.links:
    href = link.get("href", "")
    if href.startswith("#"):
        assert href[1:] in ids, f"Broken hash link: {href}"
    if href.startswith("http"):
        assert "develop-coaching.com/privacy/" in href or "develop-coaching.com/corporate-structure-notice/" in href, f"Unexpected external authored link: {href}"

for img in a.images:
    assert img.get("alt") is not None, f"Image missing alt: {img}"
    src = img.get("src", "")
    assert (ROOT / src).exists(), f"Missing local asset: {src}"

print(f"PASS: 1 h1, 1 main, {len(a.ids)} unique IDs, {len(a.links)} links, {len(a.images)} local images")
