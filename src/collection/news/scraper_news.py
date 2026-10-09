import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).parent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _extract_real_url(bing_link: str) -> str:
    """Bing RSS link membungkus URL asli artikel di query param `url=`."""
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(bing_link).query)
    return qs["url"][0] if "url" in qs else bing_link


def search_news(query: str, limit: int) -> list[dict]:
    """Cari berita lewat Bing News RSS (gratis, tanpa API key).

    Output mengikuti kontrak bersama RawDocument{source, text, metadata}
    (lihat root CLAUDE.md) supaya bisa langsung dikonsumsi oleh
    /backend/pipeline/integration.py tanpa branching per-source.
    """
    url = f"https://www.bing.com/news/search?q={urllib.parse.quote(query)}&format=rss"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()

    root = ET.fromstring(raw)
    items = root.findall(".//item")[:limit]

    results = []
    for item in items:
        title = item.findtext("title") or ""
        description = item.findtext("description") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""

        source_name = ""
        for child in item:
            if child.tag.endswith("Source"):
                source_name = child.text or ""
                break

        results.append(
            {
                "source": "news",
                "text": description,
                "metadata": {
                    "title": title,
                    "url": _extract_real_url(link),
                    "published_at": pub_date,
                    "source_name": source_name,
                },
            }
        )

    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Scrape berita dari Bing News RSS.")
    parser.add_argument("-q", "--query", default="student", help="Kata kunci pencarian")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Jumlah berita yang diambil")
    parser.add_argument("-o", "--output", default="output.json", help="Nama file JSON output")
    args = parser.parse_args()

    results = search_news(args.query, args.limit)

    output_path = HERE / args.output
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Selesai. {len(results)} berita disimpan ke {output_path}")


if __name__ == "__main__":
    main()
