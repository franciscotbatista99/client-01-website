"""Tests for initial tasks of client 1 website

To run tests:  python3 -m pytest tests -q
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[1] / "site"
INDEX = SITE / "index.html"

COMPANY_NAME = "Nordwerk Industrie-Service"
MAIN_STATEMENT = "Praktische Unterstützung für Ihren technischen Betrieb."
FIRST_SERVICE = {"Wartungsplanung": "Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe."}
MAILTO = "mailto:kontakt@nordwerk.example"
LINK_TEXT = "Anfrage stellen"
COURSE_NOTICE = "Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme."


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class Page(HTMLParser):
    """Sammelt sichtbaren Text, Überschriften, Links und lokale Assets."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.title = ""
        self.texts: list[str] = []
        self.headings: dict[str, list[str]] = {}
        self.links: list[dict[str, str]] = []
        self.assets: list[str] = []
        self._stack: list[str] = []
        self._buf: dict[str, list[str]] = {}
        self._link: dict[str, str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag in {"h1", "h2", "h3", "title"}:
            self._buf[tag] = []
        if tag == "a":
            self._link = {"href": a.get("href") or "", "text": ""}
        if tag == "link" and a.get("href"):
            self.assets.append(a["href"])
        if tag in {"script", "img"} and a.get("src"):
            self.assets.append(a["src"])
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
        if tag in self._stack:
            while self._stack and self._stack.pop() != tag:
                pass

    def handle_data(self, data):
        if self._stack and self._stack[-1] in {"script", "style"}:
            return
        self.texts.append(data)
        for buf in self._buf.values():
            buf.append(data)
        if self._link is not None:
            self._link["text"] += data

    @property
    def body_text(self) -> str:
        return norm(" ".join(self.texts))


@pytest.fixture(scope="module")
def page() -> Page:
    assert INDEX.is_file(), f"{INDEX} fehlt"
    p = Page()
    p.feed(INDEX.read_text(encoding="utf-8"))
    return p


def test_company_name_is_main_heading(page):
    assert COMPANY_NAME in page.headings.get("h1", []), "Firmenname (N-01) muss als <h1> erscheinen"


def test_claim_is_visible(page):
    assert MAIN_STATEMENT in page.body_text, "Hauptaussage (N-02) fehlt"


def test_at_least_one_service_with_required_text(page):
    found = [name for name, text in FIRST_SERVICE.items()
             if name in page.headings.get("h3", []) and text in page.body_text]
    assert found, "Mindestens eine Leistung (N-03..N-05) mit <h3> und Pflichttext fehlt"


def test_contact_link_targets_mailto(page):
    matches = [l for l in page.links if l["text"] == LINK_TEXT]
    assert matches, f'Link mit Text "{LINK_TEXT}" fehlt'
    assert all(l["href"] == MAILTO for l in matches), f"Kontaktlink muss auf {MAILTO} zeigen"


def test_exercise_notice_is_visible(page):
    assert COURSE_NOTICE in page.body_text, "Übungshinweis (N-09) fehlt"


def test_document_language_and_title(page):
    assert page.lang == "de"
    assert page.title


def test_local_assets_exist_and_no_external_resources(page):
    for ref in page.assets:
        assert not re.match(r"^(https?:)?//", ref), f"Externe Ressource nicht erlaubt: {ref}"
        assert (SITE / ref).is_file(), f"Lokales Asset fehlt: {ref}"
