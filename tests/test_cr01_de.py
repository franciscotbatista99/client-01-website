"""CR-01 (Session 5): checks for the new content on the German page site/index.html.

Runs without Factory, LLM or database:  python3 -m pytest tests -q
AC-01..AC-08 stay covered by test_site.py (regression); these tests only cover what CR-01 adds
to the German view: the third target group and the language switch to the English page.
Named test_cr01_* so the Factory does not count them towards AC-01..AC-08.
"""

from __future__ import annotations

import pytest

from test_site import AUDIENCES, INDEX, Page

NEW_AUDIENCE = "Technische Einkaufsabteilungen"
ENGLISH_PAGE = "en.html"


@pytest.fixture(scope="module")
def de() -> Page:
    p = Page()
    p.feed(INDEX.read_text(encoding="utf-8"))
    return p


def test_cr01_de_new_target_group_is_listed(de):
    assert NEW_AUDIENCE in de.list_items, f"Target group {NEW_AUDIENCE!r} missing on the German page"


def test_cr01_de_existing_target_groups_are_kept(de):
    for name in AUDIENCES:
        assert name in de.list_items, f"Existing target group {name!r} must stay on the German page"


def test_cr01_de_navigation_has_language_switch(de):
    targets = {href.split("#")[0] for href in de.nav_links}
    assert ENGLISH_PAGE in targets, f"German navigation must link to the English page ({ENGLISH_PAGE})"


def test_cr01_de_language_switch_is_labelled(de):
    labels = [link["text"] for link in de.links if link["href"].split("#")[0] == ENGLISH_PAGE]
    assert "English" in labels, 'Language switch to en.html must be labelled "English"'
