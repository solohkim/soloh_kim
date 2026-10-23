***PHP Issues Emergency Patches for Two Critical PHP2Shell RCE Flaws as Exploit Attempts Emerge***

![shell](/writeups/images/php2shell.gif)


PHP has released emergency updates that fix two critical flaws in the language itself, letting an attacker without an account run code on a web server. The fixes are in PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35, and the PHP team says only updating fully protects a server.

The flaws, together called PHP2Shell, sit in the PHP runtime, not in any application, so a site is exposed even when its own code is secure. The risk is highest on servers using Apache's mod_php, where a working exploit triggers the attack before any application code runs.

Both flaws are rated 9.2 on the CVSS v4.0 scale and carry the identifiers CVE-2026-109618 and CVE-2026-109619. PHP published them around the scheduled release time of 14:00 UTC on October 21, a day after details leaked ahead of a planned October 22 disclosure.

Researchers at Wiz, Calif, and OpenAI found and reported the flaws, which affect nearly every PHP version back to PHP 5.4.


### Who Is Affected

Every PHP installation that serves web requests is at risk, including PHP-FPM, Apache mod_php, php-cgi, FrankenPHP and LiteSpeed, according to the PHP security advisory.

Because the flaws are in the engine rather than in any site's code, even a simple "Hello World" page on a vulnerable PHP version can be attacked.

The advisory singles out mod_php as the highest risk, with a demonstrated exploit in which a single unauthenticated request triggers the attack before any application code runs. PHP-FPM behaves differently, because it shuts the worker down when a request fails early in setup.

For one of the two flaws, PHP's own analysis supports that FPM is susceptible but says no complete FPM exploit has been shown; the second flaw was shown to reach code execution on both mod_php and PHP-FPM, though the FPM path there depends on an operation inside the running application.

An attacker can also read memory from the PHP worker process, which may hold passwords, authentication tokens, API keys, and certificates belonging to other requests, without first gaining code execution.

### What to Install

Update the PHP runtime that serves web requests, then restart Apache, PHP-FPM, and any long-running PHP workers. Updating an application such as WordPress or Laravel does not update the PHP runtime beneath it; that comes from the server package, the host, or the container image.
``` bash
PHP branch	Vulnerable	First fixed version
8.5	below 8.5.12	8.5.12
8.4	below 8.4.27	8.4.27
8.3	below 8.3.36	8.3.36
8.2	below 8.2.35	8.2.35
```
PHP 8.1 and older no longer receive updates from the PHP project, and PHP 8.2 reaches end of life on December 31, 2026. For the older branches, the PHP security team has published source backports for PHP 7.4, 8.0, and 8.1 to help people building from source or waiting on a vendor.

Linux distributions and long-term-support vendors received the patches in advance, so a distribution package can carry the fix under an old-looking version number; check the package changelog for the CVE, as Debian advises, not the version string.

If You Cannot Update Yet
Only updating is a complete fix. The measures below reduce exposure to specific attack paths and do not make a server safe, according to the advisory.

For ***CVE-2026-109618***, set memory_limit=-1 so applications cannot override it, keep post_max_size low, and enforce request-size limits at the web server or proxy. Do not use RLIMIT_AS or RLIMIT_DATA as a substitute, because PHP warns they can trigger the same vulnerable path.

For CVE-2026-109619, set session.upload_progress.enabled=0 and restart every worker, and on PHP 8.5 also set fatal_error_backtraces=0. Turning off session upload progress blocks the confirmed session paths but not other variants, and no configuration change fully mitigates this flaw short of updating.

That setting is the one circulated as a workaround before the patch, and the release confirms it was never a complete fix. Session upload progress is turned on by default and can reach session handling before PHP finishes setting up a request, which is why it takes part in one confirmed attack path for CVE-2026-109619 and why turning it off does nothing for CVE-2026-109618.

"The only thing I can say is that the only mitigation is patching/upgrading PHP. I sadly know too much," PHP core developer Gina Peter Banyard wrote before the release, replying to someone who suggested the setting might be enough.

After updating, review your memory settings. The fix adds a new hard memory limit, and reaching it ends the process and stops shutdown handlers from running, so check memory_limit and post_max_size against what your application needs.

If you already patched but suspect an earlier break-in, the researchers suggest watching for unusual multipart requests followed by memory-limit errors or repeated HTTP 500 responses, oddly large PHPSESSID response cookies, and unexplained restarts of PHP workers.

***Is It Being Attacked***
Before the patch shipped, Cloudflare said it was seeing early attempts to exploit the flaws. "We are seeing early attacks emerging and are updating mitigations as new vectors show up," Cloudflare CTO Dane Knecht said, calling the firewall rules Cloudflare deployed a stopgap and urging administrators to patch.

No source has confirmed a successful break-in. watchTowr, which reproduced ***CVE-2026-109618***, reported no exploitation in the wild as of 11:26 UTC on October 21, and neither flaw was in CISA's Known Exploited Vulnerabilities catalog at that time.

Some organizations took services offline as a precaution rather than in response to any break-in. BambooHR took its service offline across the United States, Canada and Ireland, warned that payroll would be interrupted, and said it did not yet have a restoration time.

In the Netherlands, MijnOverheid, DigiD, the lower house of parliament's site, the national cyber-security center and several education systems went offline, the broadcaster NOS reported; the centre said it had not seen the flaw abused but urged everyone to patch.

### How It Came Out
A leak pulled the release forward. On October 20, as The Hacker News reported, a post on Hacker News said two PHP remote code execution flaws, with the two CVE identifiers, were set for disclosure on October 22, on no more than a trusted tip.

PHP posted an advance notice that evening and moved the release to October 21. The leak's claim of a CVSS 10.0 score was not PHP's; PHP rates both flaws 9.2.

The flaws were found by Wiz Research, Calif, and OpenAI's Codex Security team, working with the PHP security team and Google's Gemini team on the fix. The underlying code had been in PHP for more than a decade.

The researchers say AI models helped turn these long-standing flaws into working exploits, letting one researcher do in about a week what they say would otherwise have taken a team months.

Calif, which traced the bug's lineage to PHP research from 2004, says knowing the target's history still mattered, and that current models do not reliably start from obscure, twenty-year-old primitives on their own.

***Update:*** watchTowr Reports Exploitation Attempts, Still No Confirmed Break-In
watchTowr, which earlier in the day reported seeing none, said in a new advisory at 14:19 UTC on October 21 that it is observing "active exploitation attempts" of both CVE-2026-109618 and CVE-2026-109619. Cloudflare said it saw attack traffic against its customers and watched attackers change their payloads to get around its firewall rules, which it had switched on by default at 03:02 UTC, before the patch. No source has reported a confirmed break-in of a specific server as of this update.

The PHP Foundation said the coordinated disclosure came apart before the release. Around 20:00 UTC on October 20, the research firm Calif mistakenly posted a video of its working proof of concept, and at 07:41 UTC on October 21, about six hours before the fix shipped, the vendor Chainguard published built images containing the patch, letting anyone study the fix while other users waited to update.

***Update:*** PHP Foundation Says a 2024 Audit Found the First Signs of the Flaw
In the same post, the PHP Foundation said a core developer first found signs of the out-of-memory flaw behind CVE-2026-109618 during PHP's 2024 external audit, but a working attack was only theorized and no concrete route to code execution was found then.

Competing fixes each risked breaking compatibility, opening denial-of-service paths, or forcing changes on third-party extensions, and a small team struggled to agree, so work on a fix stalled for months. The Foundation called the delay "a structural failure" of its decision process and its resources.

The 2026 reports from Calif, OpenAI and Wiz, which used AI tools, established the working exploit that made the flaw's full impact clear and moved the fix to the top of the queue. The Foundation said it has since changed how it makes security decisions and added staff and tooling to catch similar problems sooner.

