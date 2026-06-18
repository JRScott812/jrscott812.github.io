# JRScott812.GitHub.io

Personal portfolio site built with [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/).

## Local development

Requirements: Ruby (2.7+), Bundler.

```bash
gem install bundler
bundle install
bundle exec jekyll serve --livereload
```

Then open http://127.0.0.1:4000 in your browser.

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
