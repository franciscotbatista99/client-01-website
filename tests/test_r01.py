"""R-01 reference check (baseline experiment only, branch r01-baseline; not part of the customer release)."""
from test_site import INDEX, Page

CARD = "Projektkoordination"
TEXT = "Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team."


def _page() -> Page:
    p = Page()
    p.feed(INDEX.read_text(encoding="utf-8"))
    return p


def test_r01_new_card_with_exact_text():
    p = _page()
    assert CARD in p.headings.get("h3", []), "Karte 'Projektkoordination' fehlt als <h3>"
    assert TEXT in p.body_text, "Text der Karte 'Projektkoordination' fehlt oder weicht ab"


def test_r01_card_is_last_of_four_services():
    p = _page()
    assert p.headings.get("h3", []) == ["Wartungsplanung", "Ersatzteilkoordination", "Betriebsdokumentation", CARD]
