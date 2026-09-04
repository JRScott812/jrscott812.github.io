#!/usr/bin/env python3
"""Generate Jekyll project pages from the owner's public GitHub repositories."""

import json
import os
import re
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "_projects"
GENERATED_DIR = PROJECTS_DIR / "generated"
OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "JRScott812")
PAGES_REPOSITORY = os.environ.get("PAGES_REPOSITORY", f"{OWNER}.github.io").lower()


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def yaml_string(value):
    return json.dumps(str(value), ensure_ascii=True)


def github_repositories():
    repositories = []
    page = 1
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "jrscott812.github.io-project-generator",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        query = urllib.parse.urlencode({"per_page": 100, "sort": "updated", "page": page})
        url = f"https://api.github.com/users/{urllib.parse.quote(OWNER)}/repos?{query}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            batch = json.load(response)
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
        page += 1


def has_github_pages(repository):
    url = f"https://api.github.com/repos/{repository['full_name']}/pages"
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "jrscott812.github.io-project-generator",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(request):
            return True
    except HTTPError as error:
        if error.code == 404:
            return False
        raise


def authored_slugs():
    return {
        path.stem.lower()
        for path in PROJECTS_DIR.glob("*.md")
        if path.is_file()
    }


def render(repository):
    name = repository["name"]
    title = name.replace("-", " ").replace("_", " ").title()
    description = repository.get("description") or f"{title}, a project by {OWNER}."
    homepage = repository.get("homepage")
    links = [
        "  - label: GitHub",
        f"    url: {yaml_string(repository['html_url'])}",
        "    style: primary",
    ]
    if homepage and homepage != repository["html_url"]:
        links.extend([
            "  - label: Visit site",
            f"    url: {yaml_string(homepage)}",
            "    style: secondary",
        ])
    social_preview = f"https://opengraph.githubassets.com/1/{repository['full_name']}"

    return "\n".join([
        "---",
        f"title: {yaml_string(title)}",
        "category: GitHub Projects",
        f"image: {yaml_string(social_preview)}",
        f"excerpt: {yaml_string(description)}",
        "links:",
        *links,
        "published: true",
        "---",
        "",
    ])


def main():
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    for path in GENERATED_DIR.glob("*.md"):
        path.unlink()

    authored = authored_slugs()
    generated = 0
    for repository in github_repositories():
        if (
            repository.get("fork")
            or repository.get("archived")
            or repository.get("name", "").lower() == PAGES_REPOSITORY
            or not has_github_pages(repository)
        ):
            continue

        slug = slugify(repository["name"])
        if slug in authored:
            continue
        (GENERATED_DIR / f"{slug}.md").write_text(render(repository), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} project page(s) from {OWNER}'s GitHub repositories.")


if __name__ == "__main__":
    main()