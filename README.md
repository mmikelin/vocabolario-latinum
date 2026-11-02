# Vocabolario Latinum

Latin–Italian vocabulary from the course *Grundlagen Latein Express* (HS 2022), with a search page:

**https://mmikelin.github.io/vocabolario-latinum/**

## Search page

- **Cerca** – search for a Latin word or an Italian meaning, optionally within one lesson.
  Capitals, macrons and hyphens don't matter: `amicus` finds *amīcus*, `sustinere` finds *sus-tinēre*.
- **Analizza un testo** – paste a Latin text and every word or phrase (like *rēs pūblica*) is looked up,
  with how often it occurs. *Copia elenco* copies the result in the same format as the script below.

Only dictionary forms are in the vocabulary, so inflected forms (*amīcum*) are not found.

## Command line

```bash
python3 vocabolario_latinum.py
```

Type one or more words, or paste a sentence; `q` quits. No packages needed.

## Data

Each `L_NN.txt` is one lesson; `composti_*.txt` are compound verbs. Entries look like this:

```
amīcus
—
amicī m.

amico
sostenitore politico
————————————
```

Every push to `main` rebuilds the page with GitHub Actions: `build_site.py` reads the `.txt` files
with the same rules as the script and writes `_site/vocabolario.json` next to `web/index.html`.

To preview locally:

```bash
python3 build_site.py && python3 -m http.server 8765 -d _site
```
