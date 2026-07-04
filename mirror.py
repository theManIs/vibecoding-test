#!/usr/bin/env python3
import os
import re
import subprocess
import urllib.parse
from pathlib import Path

BASE = "https://usmanovafit.gymteam.ru"
START = f"{BASE}/mainpage"
OUT = Path(__file__).parent / "site"

seen = set()


def curl(url: str) -> bytes | None:
    result = subprocess.run(["curl", "-fsSL", url], capture_output=True)
    if result.returncode != 0:
        return None
    return result.stdout


def abs_url(base: str, link: str) -> str:
    return urllib.parse.urljoin(base, link)


def is_local(url: str) -> bool:
    host = urllib.parse.urlparse(url).netloc
    return host in ("", "usmanovafit.gymteam.ru")


def fetch_url(url: str) -> str:
    p = urllib.parse.urlparse(url)
    return f"{p.scheme}://{p.netloc}{p.path}"


def disk_path(url: str) -> Path:
    p = urllib.parse.urlparse(url)
    path = p.path or "/index.html"
    if path.endswith("/"):
        path += "index.html"
    return OUT / path.lstrip("/")


def extract_links(text: str, base: str) -> set[str]:
    links = set()
    for pat in (
        r'(?:src|href|data-src|data-img-src)\s*=\s*["\']([^"\']+)["\']',
        r'url\(\s*["\']?([^"\')\s]+)["\']?\s*\)',
    ):
        for raw in re.findall(pat, text, re.I):
            if raw.startswith(("data:", "javascript:", "#", "mailto:", "tel:")):
                continue
            if any(x in raw for x in ("[", "]", "+", " ", "function")):
                continue
            links.add(abs_url(base, raw))
    return links


def download(url: str):
    clean = fetch_url(url)
    if clean in seen:
        return
    seen.add(clean)
    if not clean.startswith(BASE):
        return
    data = curl(url)
    if data is None:
        print("FAIL", url)
        return
    path = disk_path(clean)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print("OK", path.relative_to(OUT))
    if path.suffix.lower() in {".css", ".js", ".html"} or path.name == "mainpage":
        text = data.decode("utf-8", errors="replace")
        for link in extract_links(text, url):
            if is_local(link):
                full = abs_url(BASE, link) if not urllib.parse.urlparse(link).netloc else link
                if full.startswith(BASE):
                    download(full)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    download(START)
    src = disk_path(START)
    if src.exists():
        (OUT / "index.html").write_bytes(src.read_bytes())
    print("DONE", len(seen), "files")


if __name__ == "__main__":
    main()
