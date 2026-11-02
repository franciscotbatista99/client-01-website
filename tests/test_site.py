"""Produktchecks Nordwerk Website (Release Candidate, AC-01 bis AC-08).

Läuft ohne Factory, LLM oder Datenbank:  python3 -m pytest tests -q
Prüft statisches HTML/CSS mit der Python-Standardbibliothek.

Prüffamilien (Termin 4, Abschnitt 3):
  A  Pflichtinhalt            test_ac01_*, test_ac02_*, test_ac03_*, test_ac04_exercise_notice_*
  B  Kontakt-/Navigationsziel test_ac04_contact_*, test_ac05_*
  C  Lokale Verweise/Assets   test_ac05_internal_*, test_ac05_local_*
  Ergänzend (automatisierbar): test_ac06_* (Viewport/CSS-Heuristik), test_ac07_* (Struktur),
  test_ac08_* (eigenständiger Start). 375/1280 px und Tastatur/Fokus werden zusätzlich
  im Browser geprüft (siehe docs/browser-review.md).

Namenskonvention test_acNN_*: die Factory ordnet Ergebnisse darüber den Akzeptanzkriterien zu.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
INDEX = SITE / "index.html"
CSS = SITE / "styles.css"

N01 = "Nordwerk Industrie-Service"
N02 = "Praktische Unterstützung für Ihren technischen Betrieb."
SERVICES = {
    "Wartungsplanung": "Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.",
    "Ersatzteilkoordination": "Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen und Lieferterminen.",
    "Betriebsdokumentation": "Wir bringen technische Unterlagen in eine nachvollziehbare und nutzbare Struktur.",
}
AUDIENCES = ["Kleine Produktionsbetriebe", "Technische Serviceunternehmen"]
N07 = "Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang und nachvollziehbare Ergebnisse."
MAILTO = "mailto:kontakt@nordwerk.example"
LINK_TEXT = "Anfrage stellen"
N09 = "Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme."
NAV_TARGETS = {"#leistungen", "#kontakt"}  # AC-05: Navigation führt zu Leistungen und Kontakt


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class Page(HTMLParser):
    """Sammelt sichtbaren Text, Überschriften, Links, IDs, Bilder und lokale Assets."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.title = ""
        self.texts: list[str] = []
        self.headings: dict[str, list[str]] = {}
        self.heading_levels: list[int] = []
        self.links: list[dict[str, str]] = []
        self.nav_links: list[str] = []
        self.ids: set[str] = set()
        self.assets: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.list_items: list[str] = []
        self.meta_viewport = False
        self._stack: list[str] = []
        self._buf: dict[str, list[str]] = {}
        self._link: dict[str, str] | None = None
        self._li: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if a.get("id"):
            self.ids.add(a["id"])
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "title"}:
            self._buf[tag] = []
            if tag != "title":
                self.heading_levels.append(int(tag[1]))
        if tag == "a":
            self._link = {"href": a.get("href") or "", "text": ""}
            if "nav" in self._stack:
                self.nav_links.append(a.get("href") or "")
        if tag == "li":
            self._li = []
        if tag == "link" and a.get("href"):
            self.assets.append(a["href"])
        if tag in {"script", "img", "source"} and a.get("src"):
            self.assets.append(a["src"])
        if tag == "img":
            self.images.append({"src": a.get("src"), "alt": a.get("alt")})
        if tag == "meta" and a.get("name") == "viewport":
            self.meta_viewport = "width=device-width" in (a.get("content") or "")
        if tag not in {"meta", "link", "img", "br", "hr", "input", "source"}:
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self._buf:
            text = norm("".join(self._buf.pop(tag)))
            if tag == "title":
                self.title = text
            else:
                self.headings.setdefault(tag, []).append(text)
        if tag == "a" and self._link is not None:
            self._link["text"] = norm(self._link["text"])
            self.links.append(self._link)
            self._link = None
        if tag == "li" and self._li is not None:
            self.list_items.append(norm("".join(self._li)))
            self._li = None
        if tag in self._stack:
            while self._stack and self._stack.pop() != tag:
                pass

    def handle_data(self, data):
        if self._stack and self._stack[-1] in {"script", "style", "title"}:
            if self._stack[-1] == "title":
                self._buf.get("title", []).append(data)
            return
        self.texts.append(data)
        for key, buf in self._buf.items():
            if key != "title":
                buf.append(data)
        if self._link is not None:
            self._link["text"] += data
        if self._li is not None:
            self._li.append(data)

    @property
    def body_text(self) -> str:
        return norm(" ".join(self.texts))


@pytest.fixture(scope="module")
def page() -> Page:
    assert INDEX.is_file(), f"{INDEX} fehlt"
    p = Page()
    p.feed(INDEX.read_text(encoding="utf-8"))
    return p


# --------------------------------------------------------------------------- #
# Familie A – Pflichtinhalt
# --------------------------------------------------------------------------- #
def test_ac01_company_name_is_main_heading(page):
    assert N01 in page.headings.get("h1", []), "Firmenname (N-01) muss als <h1> erscheinen"


def test_ac01_claim_is_visible(page):
    assert N02 in page.body_text, "Hauptaussage (N-02) fehlt"


@pytest.mark.parametrize("name", list(SERVICES))
def test_ac02_service_with_required_text(page, name):
    assert name in page.headings.get("h3", []), f"Leistung {name!r} fehlt als <h3>"
    assert SERVICES[name] in page.body_text, f"Pflichttext zu {name!r} fehlt (N-03..N-05)"


@pytest.mark.parametrize("group", AUDIENCES)
def test_ac03_audience_is_listed(page, group):
    assert group in page.list_items, f"Zielgruppe {group!r} (N-06) fehlt als Listeneintrag"


def test_ac03_working_method_is_visible(page):
    assert N07 in page.body_text, "Arbeitsweise (N-07) fehlt"


def test_ac03_no_invented_numbers(page):
    """Keine erfundenen Reaktionszeiten, Kundenzahlen oder Erfolgszahlen: Pflichttexte enthalten keine Ziffern."""
    digits = re.findall(r"[^\s]*\d[^\s]*", page.body_text)
    assert not digits, f"Unerwartete Zahlen im sichtbaren Text (erfundene Angaben?): {digits}"


def test_ac04_exercise_notice_is_visible(page):
    assert N09 in page.body_text, "Übungshinweis (N-09) fehlt"


# --------------------------------------------------------------------------- #
# Familie B – Kontakt- und Navigationsziel
# --------------------------------------------------------------------------- #
def test_ac04_contact_link_targets_mailto(page):
    matches = [l for l in page.links if l["text"] == LINK_TEXT]
    assert matches, f'Link mit Text "{LINK_TEXT}" fehlt'
    assert all(l["href"] == MAILTO for l in matches), f"Kontaktlink muss auf {MAILTO} zeigen"


def test_ac04_no_other_mail_targets(page):
    others = {l["href"] for l in page.links if l["href"].startswith("mailto:") and l["href"] != MAILTO}
    assert not others, f"Unerwartete Mailziele: {others}"


def test_ac05_navigation_leads_to_services_and_contact(page):
    assert page.nav_links, "Keine Navigation (<nav> mit Links) gefunden"
    missing = NAV_TARGETS - set(page.nav_links)
    assert not missing, f"Navigation führt nicht zu: {missing}"


# --------------------------------------------------------------------------- #
# Familie C – Lokale Verweise und Assets
# --------------------------------------------------------------------------- #
def test_ac05_internal_anchors_resolve(page):
    broken = [l["href"] for l in page.links if l["href"].startswith("#") and l["href"][1:] not in page.ids]
    assert not broken, f"Interne Sprungmarken ohne Ziel-ID: {broken}"


def test_ac05_local_links_and_assets_exist(page):
    refs = page.assets + [l["href"] for l in page.links
                          if l["href"] and not l["href"].startswith(("#", "mailto:"))]
    for ref in refs:
        assert not re.match(r"^(https?:)?//", ref), f"Externe Ressource/Link nicht erlaubt: {ref}"
        assert (SITE / ref.split("#")[0]).is_file(), f"Lokaler Verweis ohne Datei: {ref}"


# --------------------------------------------------------------------------- #
# Ergänzend – AC-06 Darstellung (Heuristik; Browserreview ist maßgeblich)
# --------------------------------------------------------------------------- #
def test_ac06_viewport_meta_present(page):
    assert page.meta_viewport, '<meta name="viewport" content="width=device-width, ..."> fehlt'


def test_ac06_no_fixed_widths_wider_than_small_screens():
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.DOTALL)
    css = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)  # media-spezifische Regeln ausnehmen
    wide = [f"{prop}: {value}px" for prop, value in re.findall(r"(?<![-\w])(width|min-width)\s*:\s*(\d+)px", css)
            if int(value) > 375]
    assert not wide, f"Feste Breiten > 375 px verursachen horizontalen Überlauf: {wide}"


# --------------------------------------------------------------------------- #
# Ergänzend – AC-07 Struktur und Zugänglichkeit
# --------------------------------------------------------------------------- #
def test_ac07_document_language_and_title(page):
    assert page.lang == "de"
    assert page.title


def test_ac07_exactly_one_h1_and_no_skipped_heading_levels(page):
    assert page.heading_levels.count(1) == 1, "Genau eine <h1> erwartet"
    skips = [(a, b) for a, b in zip(page.heading_levels, page.heading_levels[1:]) if b > a + 1]
    assert not skips, f"Übersprungene Überschriftenebenen: {skips}"


def test_ac07_images_have_alt_text(page):
    missing = [img["src"] for img in page.images if not (img["alt"] or "").strip()]
    assert not missing, f"Bilder ohne Alternativtext: {missing}"


def test_ac07_visible_keyboard_focus_style():
    css = CSS.read_text(encoding="utf-8")
    assert re.search(r":focus(-visible)?\s*[,{]", css), "Kein Fokus-Stil (:focus/:focus-visible) im CSS"
    assert not re.search(r"outline\s*:\s*(none|0)\b", css), "Fokus-Outline wird entfernt"


# --------------------------------------------------------------------------- #
# Ergänzend – AC-08 Eigenständiger Start
# --------------------------------------------------------------------------- #
def test_ac08_readme_documents_start_and_test():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "http.server" in readme, "Startbefehl fehlt in der README"
    assert "pytest tests" in readme, "Testbefehl fehlt in der README"


def test_ac08_product_has_no_factory_or_llm_dependency():
    code = "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*")
                     if p.is_file() and p.suffix in {".py", ".html", ".js", ".css"} and ".venv" not in p.parts
                     and p.name != "test_site.py")
    for needle in ("src.agents", "langchain", "langgraph", "ollama", "psycopg"):
        assert needle not in code, f"Produkt hängt von Factory/LLM/DB ab: {needle}"
