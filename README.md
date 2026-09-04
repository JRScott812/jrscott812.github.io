# JRScott812.GitHub.io

Personal portfolio site built with [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/).

## Local development

Requirements: Ruby (3.x), Bundler.

```bash
gem install bundler
bundle install
```

### Preview the site (recommended)

**Do not open files in `_site/` directly in your browser** — paths like `/assets/css/style.css` only work over HTTP.

Use the local dev server instead:

```bash
bundle exec jekyll serve --livereload --config _config.yml,_config_dev.yml
```

On Windows you can double-click or run [`serve.bat`](serve.bat).

Then open **http://127.0.0.1:4000** (not a `file://` path).

`_config_dev.yml` sets `url` to `http://127.0.0.1:4000` so SEO/canonical tags match local preview. Production builds use the main `_config.yml` only.

### Build without serving

```bash
bundle exec jekyll build
```

Output goes to `_site/`. To preview a build folder, serve it over HTTP:

```bash
cd _site
python -m http.server 4000
```

Then open http://127.0.0.1:4000

After the first `bundle install`, commit the generated `Gemfile.lock` for reproducible builds.

## Adding projects

Create a markdown file in `_projects/` with front matter. Set `published: true` to show it on the Projects page.

Example:

```yaml
---
title: My Project
category: Browser Extensions
image: https://example.com/logo.png
excerpt: Short description shown on the project card.
links:
  - label: GitHub
    url: https://github.com/JRScott812/my-project
    style: primary
  - label: Live demo
    url: https://example.com
    style: secondary
published: true
tags:
  - javascript
  - chrome-extension
---

Optional longer description for the project detail page.
```

### Front matter fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Project name |
| `category` | Yes | Section heading on the Projects page (e.g. `Browser Extensions`, `Websites/Web Apps`, `Misc`) |
| `excerpt` | Yes | Short summary for cards and SEO |
| `image` | No | Logo or preview URL, or a local path like `/assets/images/my-logo.svg` |
| `links` | No | List of `{ label, url, style }` buttons (`style`: `primary` or `secondary`) |
| `published` | No | Set to `true` to include on the site (defaults to hidden if omitted) |
| `tags` | No | Optional tags shown on the project detail page |

Projects appear grouped by `category` on `/projects/`. Each file also gets a detail page at `/projects/<filename>/`.

### Automatic GitHub projects

The Pages workflow also scans the public repositories owned by `JRScott812` and generates project pages before Jekyll builds the site. Only repositories with GitHub Pages enabled are included. Forked repositories, archived repositories, and this portfolio repository are skipped. A generated page is not created when a matching hand-authored file already exists in `_projects/`, so hand-authored entries take precedence.

Generated files are stored in `_projects/generated/` and committed by the automatic sync workflow. Run the same step locally with:

```bash
python3 scripts/generate_projects.py
```

Set `GITHUB_REPOSITORY_OWNER` to scan another GitHub account. Repository descriptions become excerpts, generated pages use GitHub's Open Graph social preview image, and each page links to GitHub plus its configured homepage when one exists. The workflow runs daily and can also be started manually from the Actions tab.

## Site configuration

- Production URL: `https://jrscott812.github.io` (set in `_config.yml`)
- SEO tags via `jekyll-seo-tag`; sitemap via `jekyll-sitemap`
- Sitemap URL: `https://jrscott812.github.io/sitemap.xml` (generated at build — not committed to the repo)
- `robots.txt` points crawlers to that sitemap

The sitemap is built automatically and includes all pages plus each project in `_projects/`. To preview locally:

```bash
bundle exec jekyll build
# open _site/sitemap.xml
```

## Deployment

The site deploys via [GitHub Actions](.github/workflows/pages.yml) using Node 24–compatible action versions (`checkout@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`).

**One-time setup** (if you still use the legacy “Deploy from branch” builder):

1. Push this repo to `main`
2. Go to **Settings → Pages → Build and deployment**
3. Set **Source** to **GitHub Actions**
4. Select the **Deploy Jekyll site to Pages** workflow

That replaces GitHub’s built-in `pages-build-deployment` workflow, which still uses Node 20 actions and triggers the deprecation warning.
