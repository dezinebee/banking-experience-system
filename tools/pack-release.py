#!/usr/bin/env python3
"""Build the release zip: the three library files, a licence, and a short
consumer README. Attach the result to the GitHub Release for the tag.

The point is that a consumer should never have to guess which of the seven
files in assets/ are the library. Three are; the other three are documentation
site chrome. This script ships only the three.

    python3 tools/pack-release.py     (or: npm run pack:release)

Writes dist/bes-<version>.zip. dist/ is gitignored — the zip is a release
artefact, not a committed file.
"""
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION = json.loads((ROOT / "tokens" / "tokens.json").read_text())["$meta"]["version"]

# The library. Anything not on this list is site chrome or tooling.
LIBRARY = ["assets/tokens.css", "assets/bes.css", "assets/bes.js"]
THEMES = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "assets" / "themes").glob("*.css"))

CONSUMER_README = """# Banking Experience System — v{version}

The complete library: three files, no dependencies, no build step.

## Use it

Copy the files into your project and load them in this order:

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="bes.css">
<script src="bes.js"></script>

<div class="bes">
  <button class="bes-btn bes-btn--primary">Send AED 5,000.00</button>
</div>
```

Components live inside an element with `class="bes"`. `bes.js` initialises on
DOMContentLoaded and exposes `window.BES`; it is a classic script, not an ES
module, so load it with a plain `<script src>`.

## Dimensions

Set these on `<html>`:

| Attribute | Values | Default |
|---|---|---|
| `data-theme` | `light` · `dark` | follows the OS |
| `data-density` | `comfortable` · `standard` · `compact` | `standard` |
| `dir` + `lang` | `rtl` + `ar` · `ltr` + `en` | `ltr` + `en` |

## Theming

Tokens are the contract. Override `--bes-*` values; never edit `bes.css`.
A complete brand is token values and no rules — `themes/sadu.css` in this zip
is a worked example: {theme_count} overrides, zero CSS rules.

## Status — read this before shipping it

**v{version} is not human-verified.** Every gate this library passes is
automated. No screen-reader testing, no Arabic native-speaker review and no
usability testing has been carried out, and all Arabic UI copy is
machine-drafted. Accessibility is the design target, not a proven outcome.

Regulatory and compliance content is UX translation, not legal advice.

Full status, documentation and source: {repo}

## Licence

MIT — see LICENSE.md.
"""


def main() -> int:
    missing = [f for f in LIBRARY if not (ROOT / f).exists()]
    if missing:
        raise SystemExit(f"missing library file(s): {', '.join(missing)}")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"bes-{VERSION}.zip"

    readme = CONSUMER_README.format(
        version=VERSION,
        theme_count=len([l for l in (ROOT / "assets" / "themes" / "sadu.css").read_text().split("\n")
                         if "--bes-" in l]),
        repo="https://github.com/dezinebee/banking-experience-system",
    )

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in LIBRARY:
            z.write(ROOT / f, pathlib.Path(f).name)
        for t in THEMES:
            z.write(ROOT / t, f"themes/{pathlib.Path(t).name}")
        z.write(ROOT / "LICENSE.md", "LICENSE.md")
        z.writestr("README.md", readme)

    names = zipfile.ZipFile(out).namelist()
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1024:.1f} KB)")
    for n in names:
        print(f"  {n}")
    print(f"\nAttach this to the GitHub Release for tag v{VERSION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
