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