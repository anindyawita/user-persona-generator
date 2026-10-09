import argparse
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _fetch_page(app_id: str, page: int, country: str) -> list[dict]:
    url = (
        f"https://itunes.apple.com/{country}/rss/customerreviews/"
        f"page={page}/id={app_id}/sortby=mostrecent/json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.load(resp)

    entries = data.get("feed", {}).get("entry", [])
    # Apple selalu menaruh info app itu sendiri di entry[0] kalau ada review,
    # tapi kalau kosong ya sudah kosong. Kita filter yang punya im:rating
    # (entry app info gak punya field ini).
    return [e for e in entries if "im:rating" in e]


def search_reviews(app_id: str, limit: int, country: str = "us") -> list[dict]:
    """Ambil review App Store buat 1 app tertentu (bukan keyword search).

    Output mengikuti kontrak bersama RawDocument{source, text, metadata}
    (lihat root CLAUDE.md).
    """
    results = []
    page = 1
    while len(results) < limit and page <= 10:
        entries = _fetch_page(app_id, page, country)
        if not entries:
            break

        for e in entries:
            results.append(
                {
                    "source": "app_store",
                    "text": e.get("content", {}).get("label", ""),
                    "metadata": {
                        "title": e.get("title", {}).get("label", ""),
                        "rating": e.get("im:rating", {}).get("label", ""),
                        "author": e.get("author", {}).get("name", {}).get("label", ""),
                        "app_version": e.get("im:version", {}).get("label", ""),
                        "updated_at": e.get("updated", {}).get("label", ""),
                        "review_id": e.get("id", {}).get("label", ""),
                    },
                }
            )
            if len(results) >= limit:
                break
        page += 1

    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Scrape review App Store (iTunes RSS).")
    parser.add_argument("-a", "--app-id", required=True, help="Numeric App Store track ID (contoh: 570060128 untuk Duolingo)")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Jumlah review yang diambil")
    parser.add_argument("-c", "--country", default="us", help="Kode negara storefront (contoh: us, id)")
    parser.add_argument("-o", "--output", default="output_appstore.json", help="Nama file JSON output")
    args = parser.parse_args()

    results = search_reviews(args.app_id, args.limit, args.country)

    output_path = HERE / args.output
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Selesai. {len(results)} review disimpan ke {output_path}")


if __name__ == "__main__":
    main()
