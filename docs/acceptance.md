# Acceptance checklist – Release v1.0 (Session 5: CR-01 + SR-01)

| | |
|---|---|
| Candidate | `main` after merging this checklist → tag `v1.0` (`git rev-parse v1.0`) |
| Baseline | `rc-1` (`cdbcba6`), S4 release candidate |
| CR-01 Factory runs | DE and EN runs by Daniil (configs `projects/website-01-cr01-de.json`, `website-01-cr01-en.json`); run IDs, gate decisions and raw data in the Factory repo (`evidence/session-05.md`, `runs/website-01-cr01-*`); product change merged via PR #21 (`066f72c`) |
| Final check on the release state | Factory `--verify-only` run `2fb2d0dd-e75f-45b9-b0cc-2c8512b34212` on `3fa2424`: 40 passed / 0 failed, approved by Fatih (2026-11-09 ≈ 12:58 UTC), `release_status: released`, artifact sha256 `33373692…` |
| Product checks | `python3 -m pytest tests -q` → 44 passed (`test_site.py` 23 = AC-01–08 regression, `test_cr01_en.py` 17, `test_cr01_de.py` 4) |
| Browser review | Fatih, 2026-11-09 13:55–13:57 local, both views at 375/1280 px + keyboard |

| AC | Automated product check | Manual evidence | Result |
|---|---|---|---|
| AC-01 Company name + main statement | `test_ac01_*` (DE), `test_cr01_en_company_name_*`, `test_cr01_en_main_statement_*` | browser review | pass |
| AC-02 Three services with text | `test_ac02_*` | – | pass |
| AC-03 Target groups, approach, no invented promises | `test_ac03_*`, `test_cr01_de_*_target_group*`, `test_cr01_en_no_invented_numbers`, `test_cr01_en_only_required_texts` | browser review | pass |
| AC-04 Contact link + course notice | `test_ac04_*`, `test_cr01_en_contact_*`, `test_cr01_en_notice_*` | contact link usable in both views | pass |
| AC-05 Navigation, internal links, local assets | `test_ac05_*`, `test_cr01_en_internal_anchors_*`, `test_cr01_en_local_links_*` | nav + language switch DE ↔ EN work | pass |
| AC-06 No overflow at 375/1280 px | `test_ac06_*` (heuristic), `test_cr01_en_viewport_meta_present` | browser review both views | pass |
| AC-07 Title, lang, headings, focus | `test_ac07_*`, `test_cr01_en_language_and_title`, `test_cr01_en_exactly_one_h1_*` | keyboard/focus both views | pass |
| AC-08 Fresh checkout starts without Factory | `test_ac08_*` | fresh checkout record below | pass |
| AC-09 CR-01 met, German content/nav/contact still work | `test_cr01_en.py` (17), `test_cr01_de.py` (4), AC-01–08 regression green | browser review both views, language switch both directions | pass – minor defect: on `en.html` each service name is repeated as its description and "Request information" appears as text and as link (no factual change, open) |
| AC-10 Component inventory, SR-01 response, recorded customer acceptance | – | `docs/phpSecurityConsiderations.md` (response + component inventory, sources accessed 09/11/2026), prepared and fact-checked by Rafael and Caitlin (no independent second check); customer acceptance by the instructor, see below | pass |

## Approval

- **Technical approval (team):** Fatih, 2026-11-09 14:05 local – based on the final regression (`--verify-only` run `2fb2d0dd`, 44 product checks green), fresh checkout and browser review above; release `v1.0`
- **Customer acceptance (instructor, Prof. Clemen):** accepted, 2026-11-09 ≈ 13:40 local (recorded by the team as communicated; the decision was given on the state presented at that time, before PR #21 was merged at 13:47).
- Outstanding defects: on `en.html` the service descriptions repeat the service names and "Request information" appears as text and as link (cosmetic, no factual change). No further defects recorded.

## Fresh checkout record (AC-08, S5)

- By: Fatih, 2026-11-09 13:55 local (12:55 UTC), new clone in `/tmp/fresh-s5`, commit `3fa2424`
- Commands:
  ```
  git clone https://github.com/franciscotbatista99/client-01-website.git fresh-s5
  cd fresh-s5
  python -m pytest tests -q                     → 40 passed
  python3 -m http.server 8010 --directory site  → index.html, en.html, styles.css: 200
  ```
- Language switch DE → EN → DE works; no Factory, no LLM, no database running: confirmed
- (`test_cr01_de.py` added afterwards: 44 passed)

---

# Acceptance checklist – Release Candidate rc-1 (CUST-002, Session 4)

| | |
|---|---|
| Candidate | tag `rc-1` → commit `cdbcba62affa591f6974383c3065e45d4fb514b0` |
| Agent run | `37079911-0dab-49e6-a4b9-0cec9c71d06d` (Factory `runs/website-01/37079911…`), qwen3:4b `359d7dd4bcda` |
| Review diff | PR #16 (`ef904f4`), gate decision: approved by Francisco, 2026-11-02 11:46 UTC, `release_status: released` |
| Product checks | `python3 -m pytest tests -q` → 23 passed (in the run and on `rc-1`) |
| Browser review | `tests/browser_test_s4.md` |

| AC | Automated product check (`tests/test_site.py`) | Manual evidence | Result |
|---|---|---|---|
| AC-01 Company name + main statement | `test_ac01_*` (2) | gate review run 37079911 | pass |
| AC-02 Three services with text | `test_ac02_*` (3) | – | pass |
| AC-03 Target groups, approach, no invented promises | `test_ac03_*` (4, incl. no numbers) | gate review: no invented content | pass |
| AC-04 Contact link + course notice | `test_ac04_*` (3) | browser review: contact link usable | pass |
| AC-05 Navigation, internal links, local assets | `test_ac05_*` (3) | browser review: nav links jump correctly | pass |
| AC-06 No overflow at 375/1280 px | `test_ac06_*` (2, heuristic) | browser review 375/1280 px | pass |
| AC-07 Title, lang, headings, focus | `test_ac07_*` (4) | browser review keyboard/focus | pass |
| AC-08 Fresh checkout starts without Factory | `test_ac08_*` (2) | fresh checkout record below | pass |

## Fresh checkout record (AC-08)

- By: Fatih, 2026-11-02 13:36 local (12:36 UTC), on a new clone in `/tmp/fresh-check`
- Commands:
  ```
  git clone https://github.com/franciscotbatista99/client-01-website.git fresh-check
  cd fresh-check && git checkout rc-1
  python3 -m venv .venv && source .venv/bin/activate && pip install pytest
  python -m pytest tests -q        → 23 passed
  python3 -m http.server 8010 --directory site   → page loads: yes
  ```
- No Factory, no LLM, no database running: confirmed

## Controlled failure case (Factory, isolated copy of rc-1)

- Run `536b4d37`: one fault (`mailto:kontakt@nordwerk.exmaple`) → `test_ac04_contact_link_targets_mailto`, `test_ac04_no_other_mail_targets` failed → gate offered no "approved" → `not_released`
- Run `41cd73ed`: fault reverted → 23/23 → `released`, artifact hash identical to the candidate (`a7a4bbd4…`)
- The final delivery `rc-1` never contained the fault.