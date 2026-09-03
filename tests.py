from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.images = []
        self.videos = []
        self.sources = []
        self.details = 0
        self.summaries = 0
        self.h1 = 0
        self.main = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "video":
            self.videos.append(attrs)
        elif tag == "source":
            self.sources.append(attrs)
        elif tag == "details":
            self.details += 1
        elif tag == "summary":
            self.summaries += 1
        elif tag == "h1":
            self.h1 += 1
        elif tag == "main":
            self.main += 1


audit = Audit()
audit.feed(HTML)

assert audit.h1 == 1, f"Expected one h1, got {audit.h1}"
assert audit.main == 1, f"Expected one main, got {audit.main}"
assert len(audit.ids) == len(set(audit.ids)), "Duplicate IDs"
assert 'lang="en"' in HTML, "Missing page language"
assert "this isn’t just a shortcut" not in HTML.lower(), "Removed sentence returned"
assert "whatsapp" not in HTML.lower(), "WhatsApp should not be present"
assert "Book a Call" in HTML, "Primary CTA missing"
assert 'id="booking"' in HTML and 'id="booking-calendar"' in HTML, "Booking target missing"
assert "Calendar integration placeholder" in HTML, "Calendar placeholder missing"
assert "The Develop Mastermind" in HTML, "Mastermind offer missing"
assert "Five pillars. One plan." in HTML, "Five-pillar method missing"
assert "Architect Attractor™" in HTML and "Jarvis™" in HTML, "Programme toolkit missing"
assert "Your first 90 days" in HTML, "90-day plan missing"
assert audit.details == 5 and audit.summaries == 5, "FAQ accordion is incomplete"
assert "@media(max-width:680px)" in CSS, "Mobile CSS missing"
assert "prefers-reduced-motion" in CSS, "Reduced-motion handling missing"

ids = set(audit.ids)
for link in audit.links:
    href = link.get("href", "")
    if href.startswith("#"):
        assert href[1:] in ids, f"Broken hash link: {href}"
    elif href.startswith("http"):
        allowed = (
            "develop-coaching.com/privacy/" in href
            or "develop-coaching.com/corporate-structure-notice/" in href
        )
        assert allowed, f"Unexpected external authored link: {href}"
    else:
        raise AssertionError(f"Unexpected link target: {href}")

for image in audit.images:
    assert image.get("alt") is not None, f"Image missing alt: {image}"
    src = image.get("src", "")
    assert src and (ROOT / src).exists(), f"Missing local asset: {src}"

assert len(audit.videos) == 1 and len(audit.sources) == 1, "Mastermind video missing"
poster = audit.videos[0].get("poster", "")
assert poster and (ROOT / poster).exists(), f"Missing video poster: {poster}"
assert audit.sources[0].get("type") == "video/mp4", "Video source type missing"

print(
    "PASS: "
    f"1 h1, 1 main, {len(audit.ids)} unique IDs, {len(audit.links)} controlled links, "
    f"{len(audit.images)} local images, 1 video, {audit.details} FAQ items"
)
