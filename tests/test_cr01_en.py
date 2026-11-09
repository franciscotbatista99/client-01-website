"""CR-01 (Session 5): checks for the English entry page site/en.html.

Runs without Factory, LLM or database:  python3 -m pytest tests -q
Reuses the HTML parser from test_site.py. The tests are named test_cr01_* (not test_acNN_*),
so the Factory does not count them towards AC-01..AC-08; those stay covered by test_site.py
as the regression check of the German page.
"""

from __future__ import annotations

import re

import pytest

from test_site import MAILTO, SITE, Page, norm

EN = SITE / "en.html"
GERMAN_PAGE = "index.html"

TITLE = "Nordwerk Industrie-Service"
STATEMENT = "Practical support for your technical operations."
SERVICES = ["Maintenance planning", "Spare parts coordination", "Operational documentation"]
TARGET_GROUP = "Technical purchasing departments"
CONTACT_TEXT = "Request information"
NOTICE = "Fictional company – HAW Hamburg course project. No real offers or contact."

# Every visible text on the English page must come from this set: the required CR-01 texts
# plus the team's section headings and navigation labels. Anything else is invented content.
ALLOWED_TEXTS = {TITLE, STATEMENT, *SERVICES, TARGET_GROUP, CONTACT_TEXT, NOTICE,
                 "Services", "Target groups", "Contact", "Deutsch"}


@pytest.fixture(scope="module")
def en() -> Page:
    assert EN.is_file(), f"{EN} is missing"
    p = Page()
    p.feed(EN.read_text(encoding="utf-8"))
    return p


# CR-01-1: language metadata and own document title
def test_cr01_en_language_and_title(en):
    assert en.lang == "en", 'English page needs <html lang="en">'
    assert TITLE in en.title, "English page needs its own <title> with the company name"


def test_cr01_en_viewport_meta_present(en):
    assert en.meta_viewport, '<meta name="viewport" content="width=device-width, ..."> is missing'


# CR-01-2: required English content, verbatim
def test_cr01_en_company_name_is_main_heading(en):
    assert TITLE in en.headings.get("h1", []), f"{TITLE!r} must be the <h1>"


def test_cr01_en_main_statement_is_visible(en):
    assert STATEMENT in en.body_text, "Main statement is missing"


@pytest.mark.parametrize("name", SERVICES)
def test_cr01_en_service_is_listed(en, name):
    assert name in en.headings.get("h3", []), f"Service {name!r} is missing as <h3>"


def test_cr01_en_target_group_is_listed(en):
    assert TARGET_GROUP in en.list_items, f"Target group {TARGET_GROUP!r} is missing as a list item"


def test_cr01_en_notice_is_visible(en):
    assert NOTICE in en.body_text, "Course notice is missing"


# CR-01-3: contact
def test_cr01_en_contact_link_targets_mailto(en):
    matches = [l for l in en.links if l["text"] == CONTACT_TEXT]
    assert matches, f'Link with text "{CONTACT_TEXT}" is missing'
    assert all(l["href"] == MAILTO for l in matches), f"Contact link must point to {MAILTO}"


def test_cr01_en_no_other_mail_targets(en):
    others = {l["href"] for l in en.links if l["href"].startswith("mailto:") and l["href"] != MAILTO}
    assert not others, f"Unexpected mail targets: {others}"


# CR-01-5: language switch and contact reachable from the navigation
def test_cr01_en_navigation_has_language_switch_and_contact(en):
    targets = {href.split("#")[0] or href for href in en.nav_links}
    assert GERMAN_PAGE in targets, f"Navigation must link to the German page ({GERMAN_PAGE})"
    assert "#contact" in en.nav_links, "Navigation must lead to #contact"


# CR-01-6: no invented content
def test_cr01_en_no_invented_numbers(en):
    digits = re.findall(r"[^\s]*\d[^\s]*", en.body_text)
    assert not digits, f"Unexpected numbers in visible text (invented figures?): {digits}"


def test_cr01_en_only_required_texts(en):
    extra = sorted({norm(t) for t in en.texts if norm(t)} - ALLOWED_TEXTS)
    assert not extra, f"Visible text that is not part of CR-01 (invented content?): {extra}"


# Structure, links and assets (same rules as AC-05/AC-07 on the German page)
def test_cr01_en_exactly_one_h1_and_no_skipped_heading_levels(en):
    assert en.heading_levels.count(1) == 1, "Exactly one <h1> expected"
    skips = [(a, b) for a, b in zip(en.heading_levels, en.heading_levels[1:]) if b > a + 1]
    assert not skips, f"Skipped heading levels: {skips}"


def test_cr01_en_internal_anchors_resolve(en):
    broken = [l["href"] for l in en.links if l["href"].startswith("#") and l["href"][1:] not in en.ids]
    assert not broken, f"Internal anchors without a target id: {broken}"


def test_cr01_en_local_links_and_assets_exist(en):
    refs = en.assets + [l["href"] for l in en.links
                        if l["href"] and not l["href"].startswith(("#", "mailto:"))]
    for ref in refs:
        assert not re.match(r"^(https?:)?//", ref), f"External resource/link not allowed: {ref}"
        assert (SITE / ref.split("#")[0]).is_file(), f"Local reference without a file: {ref}"