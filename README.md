# Photography site

A small Hugo site: sidebar layout, a justified photo grid and a lightbox. The layout and styles are adapted from [leovan/leovan.me](https://github.com/leovan/leovan.me) (CC BY-NC-SA 4.0), so keep that credit and share under the same license.

## Add photos

1. Put the originals in `photos-src/` (ignored by git).
2. Run `python scripts/add_photos.py photos-src` (needs `pip install pillow`).
3. Commit `static/images/photography/` and `static/data/photography/`.

The script resizes each photo, makes a thumbnail, and writes one JSON file per year. The photography page shows one section per year, newest first.

## Preview

```bash
hugo server
```

## Publish

Push to `main`. In the repository settings, set Pages to "GitHub Actions". The workflow in `.github/workflows/pages.yml` builds and deploys the site.

## Make it yours

- `hugo.toml`: name, slogan, menu.
- `static/images/web/avatar.svg`: replace with your own avatar.
- `content/`: home, about and photography page text.
