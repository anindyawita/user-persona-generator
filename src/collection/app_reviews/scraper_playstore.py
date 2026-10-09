import argparse
import json
import sys
from pathlib import Path

from google_play_scraper import Sort, reviews

HERE = Path(__file__).parent


def search_reviews(app_id: str, limit: int, lang: str = "en", country: str = "us") -> list[dict]:
    """Ambil review Google Play buat 1 app tertentu (bukan keyword search).

    app_id di sini adalah package name (contoh: "com.duolingo").

    Output mengikuti kontrak bersama RawDocument{source, text, metadata}
    (lihat root CLAUDE.md).
    """
    raw_reviews, _ = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=limit,
    )

    results = []
    for r in raw_reviews:
        results.append(
            {
                "source": "play_store",
                "text": r.get("content", ""),
                "metadata": {
                    "rating": r.get("score"),
                    "author": r.get("userName", ""),
                    "app_version": r.get("appVersion", ""),
                    "thumbs_up": r.get("thumbsUpCount", 0),
                    "review_id": r.get("reviewId", ""),
                    "at": str(r.get("at", "")),
                },
            }
        )

    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Scrape review Google Play Store.")
    parser.add_argument("-a", "--app-id", required=True, help="Package name (contoh: com.duolingo)")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Jumlah review yang diambil")
    parser.add_argument("-o", "--output", default="output_playstore.json", help="Nama file JSON output")
    args = parser.parse_args()

    results = search_reviews(args.app_id, args.limit)

    output_path = HERE / args.output
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Selesai. {len(results)} review disimpan ke {output_path}")


if __name__ == "__main__":
    main()
