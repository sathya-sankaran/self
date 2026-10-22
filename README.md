# sathyasankaran.com

Source for **[sathyasankaran.com](https://www.sathyasankaran.com)**. One hand-written
`index.html`: inlined CSS, JSON-LD structured data, no JavaScript, no build, no dependencies.

## Counts

The tool and story counts (and the lists in the teasers) come from the cards. Give each new tool `<article>` or
`<a class="story">` a short `data-teaser`; the pre-commit hook runs `python3 scripts/counts.py` and the Counts check
on GitHub fails when a count is stale. After cloning, turn the hook on once: `git config core.hooksPath .githooks`.

© 1995–2026 Sathya Sankaran. All rights reserved. See [LICENSE](LICENSE). Bundled fonts (Inter Tight, JetBrains Mono) remain under the SIL Open Font License.
