### PHP Vulnerabilities
#### What are the vulnerabilities?
Two critical vulnerabilities, CVE-2026-109618 and CVE-2026-109619 have been discovered in PHP.
These vulnerabilities are believed to be present in all current versions of PHP, and at the very least in all versions from 5 onwards. They allow malicious actors to perform remote code execution (RCE). The potential consequences include the takeover of (web) servers, the loss of website accessibility, data leaks, or the disruption of specific functionalities, such as the ability to log in.
How do they work?
The vulnerability CVE-2026-109618 allows remote code execution through memory corruption during out-of-memory (OOM) handling. PHP enforces its user-configurable memory_limit by using longjmp() to abort any request that exceeds the limit, which raises an OOM error. This can interrupt PHP while internal request data is only partially initialised, for example, while parsing a form-based file upload. Request cleanup may then treat the invalid data as valid and try to free memory that was never initialised. That memory may still contain data from earlier allocations controlled by the attacker.
The vulnerability CVE-2026-109619 allows remote code execution through stale global state. Internal state owned by a request can survive after its backing memory has been freed, for example after a fatal error. A later request handled by the same worker may use that stale state before normal initialisation resets it.

#### How can these vulnerabilities be fixed?
Temporary isolation is a temporary solution that removes public access to the website, protecting it from attacks over the internet. However, this also stops the website from being available.
Static replacement is replacing the website with a static version that does not use PHP, so is not vulnerable to the PHP vulnerabilities. However, the website cannot contain any dynamic elements and it can be complex to do this conversion.
Updating is the best solution to mitigate these vulnerabilities. It is the only way to ensure that the vulnerability is patched.

#### How do these affect CMS?
CMSs that use PHP may have lost functionality for several reasons. These include the CMS being temporarily isolated or form plugins not being compatible with the patched version of PHP.

#### Is your existing site affected?
Based on the information you gave about your existing website, it is possible that it is affected. Ask your host which patch version PHP is used. If the answer is earlier than 8.2.35, then temporarily take the existing website offline and as soon as possible update this to 8.2.35. Additionally, ask the host to set session.upload_progress.enabled=0. If the website cannot be updated immediately, ask your host to complete the mitigations set out below.
If the patch version is older than 8.2.35, look for signs of compromise and for backdoors in your system.
If you have been compromised, it is important to report this through the CRA Single Reporting platform. An early warning needs to be submitted within 24 hours of becoming aware, a full notification within 72 hours, and a final report within 14 days.

#### Temporary Mitigations:
CVE-2026-109618 (OOM corruption):
Set memory_limit=-1 in a way applications cannot override
Set a low post_max_size: 8M for applications that do not need file uploads, 32M if uploads are required. Keep upload_max_filesize below post_max_size.
Use a container or cgroup memory limit as an availability boundary, preferably with a policy that kills only the affected worker. Do not use RLIMIT_AS or RLIMIT_DATA instead, because they can trigger the vulnerable allocation failure.
CVE-2026-109619 (stale global state):
Set session.upload_progress.enabled=0 and restart every worker. Apply this in php.ini, an FPM pool or a server configuration that takes effect before request parsing. Do not rely on ini_set() or FPM .user.ini. This blocks the confirmed session paths but not other variants.
On PHP 8.5, set fatal_error_backtraces=0 and restart every worker. This blocks the confirmed fatal backtrace path only.
Remove invalid or deprecated per-request settings that emit diagnostics before initialisation. Hiding diagnostics with error_reporting, display_errors or @ does not help.
Fix fatal errors and execution timeouts that attackers can reach, including failures in callbacks, upload or import processing, and cleanup.
CVE-2026-115560:
Set session.upload_progress.enabled=0 and restart every worker until the next regular bugfix release, to fully protect from CVE-2026-115560.

#### Can you safely use our website?
Yes, our website doesn't use PHP so is safe from these vulnerabilities.

#### Component Inventory
**Runtime Components (Production)**
* HTML/CSS: HTML5 / CSS3
* PHP: not used
* Database/SQL: not used
* CMS (Content Management System): not used
* Dynamic Forms: not used (replaced by mailto: link)
**Build & Test Components (Development/Local)**
* Local Server Environment: Python [3.14.6] (http.server)
* Testing Framework: pytest [9.1.1]
* Version Control: Git

#### Sources (all accessed on 09/11/2026):
https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w
https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities 
https://www.php.net/archive/2026.php
https://www.ncsc.gov.ie/pdfs/2610210276_CVE-2026-109618_CVE-2026-109619.pdf
https://www.circl.lu/pub/tr-102/
https://cert.europa.eu/publications/security-advisories/2026-018/
https://digital-strategy.ec.europa.eu/en/policies/cra-reporting
