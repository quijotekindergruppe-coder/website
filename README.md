# Quijote – Kindergruppe · Jardín infantil

Website of the bilingual (German · Spanish) playgroup Quijote, Große Neugasse 11, 1040 Wien.
The site is available in German, English and Spanish.

Every change pushed to the `main` branch is built and published automatically
(see **Actions** tab). Nobody needs to install anything to make text changes.

## Changing text

All text lives in three files, one per language:

| Language | File |
|---|---|
| Deutsch | `content/de.json` |
| English | `content/en.json` |
| Español | `content/es.json` |

To edit on github.com: open the file → click the pencil icon → change the text
between the quotation marks → **Commit changes**. The site updates about a minute later.

Rules of thumb:
- Change only the text inside `"…"`, never the names before the colon.
- A quotation mark inside a text must be written as `\"`.
- Make the same change in all three languages.
- Placeholders still to fill in are written in `[square brackets]`.

## Settings, emails and photos — `content/site.json`

- **emails** – addresses shown on the site.
- **form → route** – where each contact-form topic is sent. Today: *Available place*
  → `anmelden@quijote.at`, everything else → `quijotekindergruppe@gmail.com`.
- **team** – names of the team. To add a portrait: upload `firstname-800.jpg` and
  `firstname-1600.jpg` (square photos, 800 and 1600 px wide) to `assets/img/`, then
  set `"photo": "firstname"` and add its size under `image_sizes`.
- **images** – which photo appears where (file names in `assets/img/`, without
  the `-800.jpg` / `-1600.jpg` ending).
- **pages** – web address of each page in each language.

## Contact form

The form is delivered by [FormSubmit](https://formsubmit.co) (free, no account).
**The first message to each address triggers a confirmation email from FormSubmit**
— open it and click *Activate Form* once for `anmelden@quijote.at` and once for
`quijotekindergruppe@gmail.com`. After that, messages arrive normally.

## Going live on www.quijote.at

1. Repository **Settings → Pages**: under *Custom domain* enter `www.quijote.at` and save.
2. At the company that manages the quijote.at domain, add a DNS record:
   `www` · `CNAME` · `quijotekindergruppe-coder.github.io`
   (and forward the bare `quijote.at` to `www.quijote.at`).
3. Back in Settings → Pages, tick **Enforce HTTPS** once it becomes available.

Before going live: fill in the Impressum and the privacy policy (Datenschutzerklärung),
and collect photo consent from parents and staff.

## For developers

```
pip install -r requirements.txt
python3 build.py          # writes the finished site to _site/
python3 -m http.server -d _site 8000
```

Templates are in `templates/` (Jinja2), styles in `assets/css/style.css`, the
small script for the phone menu and form routing in `assets/js/main.js`.
