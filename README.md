# client-01-website – Nordwerk Industrie-Service

Static website for Nordwerk Industrie-Service, a fictional small B2B service provider in Hamburg (HAW Hamburg course project – no real offers or contact).

- German view: `site/index.html`
- English entry page (CR-01): `site/en.html`

## Start (AC-08)

No Factory, LLM or database is needed. Python 3 is only used as a local web server.

```bash
git clone https://github.com/franciscotbatista99/client-01-website.git
cd client-01-website
python3 -m http.server 8000 --directory site
```

Then open <http://localhost:8000> (German) and <http://localhost:8000/en.html> (English).
Alternatively open `site/index.html` directly in the browser.

## Product tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
python -m pytest tests -q
```

| File | Checks |
|---|---|
| `tests/test_site.py` | AC-01–AC-08 on the German view (required content, contact/navigation targets, local links/assets, title/lang/focus heuristics) |
| `tests/test_cr01_en.py` | CR-01: English required content, `lang="en"`, title, language switch, contact |

Manual checks (not automated): browser review at 375 px and 1280 px and keyboard/focus for both views – template `tests/browser_test_s4.md`, results in `docs/acceptance.md`.

## Structure

| Path | Content |
|---|---|
| `site/` | Website (HTML + one CSS file, no build step, no JavaScript, no external fonts/tracking) |
| `tests/` | Product tests + browser review template |
| `docs/` | Acceptance checklist, CR-01/SR-01 documents |

## Maintenance note

- **Content changes** go through the team's Factory (repo `cait33/agentic_ai`): the agent may only write between the markers `<!-- AGENT:name -->…<!-- /AGENT:name -->` (`header`, `nav`, `services`, `audiences`, `approach`, `contact`, `footer`). Structure outside the markers (sections, IDs, `<nav>`, CSS) is maintained by hand via pull request.
- **Every change** needs a pull request with review diff, green `python -m pytest tests -q` and a repeated browser review at 375/1280 px + keyboard. New requirements get a new test (`test_acNN_*`).
- **Required texts** (company name, main statement, services, target groups, contact `mailto:kontakt@nordwerk.example`, course notice) must not be changed or extended with invented figures, references or service promises.
- **Updates/dependencies:** the delivery is static HTML/CSS without server-side code, CMS or contact form; there are no runtime packages to patch. Whoever hosts the site is responsible for the web server/hosting updates (see SR-01 response and component inventory in `docs/`). Static does not automatically mean secure.
- **Releases** are marked with a git tag (`rc-1` = S4 candidate, `v1.0` = S5 release); the AC checklist in `docs/acceptance.md` belongs to the tagged commit.
