"""Angular documentation scraper for RAG pipeline."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

from src.config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AngularDocsScraper:
    """Scrapes Angular documentation from angular.dev."""

    def __init__(self, base_url: str = settings.docs_base_url) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "DocuMentor-AI/1.0"
        self.output_dir = settings.docs_output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._visited: set[str] = set()

    def scrape_all(self) -> list[dict[str, str]]:
        """Scrape all Angular documentation pages."""
        pages = []

        # Start with main docs pages
        start_urls = [
            "/",
            "/guide/quick-start",
            "/guide/understanding-angular/overview",
            "/guide/understanding-angular/architecture",
            "/guide/components",
            "/guide/templates",
            "/guide/routing",
            "/guide/forms",
            "/guide/dependency-injection",
            "/guide/observables",
            "/guide/signals",
            "/guide/standalone-components",
            "/guide/ngmodules",
            "/guide/http",
            "/guide/api",
        ]

        for path in start_urls:
            url = urljoin(self.base_url, path)
            logger.info(f"Scraping: {url}")
            doc = self._scrape_page(url)
            if doc:
                pages.append(doc)
                pages.extend(self._scrape_related(url, depth=1))

        logger.info(f"Scraped {len(pages)} pages total")
        return pages

    def _scrape_page(self, url: str) -> dict[str, str] | None:
        """Scrape a single page."""
        if url in self._visited:
            return None
        self._visited.add(url)

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = self._extract_title(soup)

        # Extract main content
        content = self._extract_content(soup)

        if not content:
            return None

        return {
            "url": url,
            "title": title,
            "content": content,
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        # Try different selectors
        for selector in ["h1", "title", ".page-title"]:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(strip=True)
        return "Untitled"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page."""
        # Find main content area
        content_elem = (
            soup.select_one("main")
            or soup.select_one("article")
            or soup.select_one(".content")
        )

        if not content_elem:
            # Fallback: get body
            content_elem = soup.body

        if not content_elem:
            return ""

        # Remove unwanted elements
        for elem in content_elem.select(
            "nav, header, footer, aside, .sidebar, .toc, script, style"
        ):
            elem.decompose()

        # Get text content
        text = content_elem.get_text(separator="\n", strip=True)

        # Clean up whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        return text

    def _scrape_related(self, base_url: str, depth: int = 1) -> list[dict[str, str]]:
        """Scrape related documentation links."""
        if depth <= 0:
            return []

        pages = []
        parsed = urlparse(base_url)

        try:
            response = self.session.get(base_url, timeout=30)
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.RequestException:
            return []

        # Find all internal links
        for link in soup.select("a[href]"):
            href = link.get("href", "")
            full_url = urljoin(base_url, href)

            # Check if same domain and not visited
            if urlparse(full_url).netloc != parsed.netloc:
                continue
            if not full_url.startswith(self.base_url):
                continue
            if full_url in self._visited:
                continue

            # Only follow docs links
            if "/guide/" not in full_url and "/api/" not in full_url:
                continue

            doc = self._scrape_page(full_url)
            if doc:
                pages.append(doc)

        return pages

    def save(self, pages: list[dict[str, str]]) -> None:
        """Save scraped pages to JSON."""
        output_file = self.output_dir / "angular_docs.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(pages)} pages to {output_file}")


def main() -> None:
    """CLI entry point."""
    scraper = AngularDocsScraper()
    pages = scraper.scrape_all()
    scraper.save(pages)
    print(f"Scraped {len(pages)} pages")


if __name__ == "__main__":
    main()
