import argparse
import asyncio
import json
import sys
from pathlib import Path

from twscrape import API

HERE = Path(__file__).parent


def load_env():
    env_path = HERE / ".env"
    if not env_path.exists():
        raise RuntimeError(
            f"File .env tidak ditemukan di {env_path}. "
            "Copy .env.example jadi .env lalu isi AUTH_TOKEN dan CT0."
        )

    values = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        values[key.strip()] = val.strip()

    if not values.get("AUTH_TOKEN") or not values.get("CT0"):
        raise RuntimeError("AUTH_TOKEN atau CT0 masih kosong di .env")

    return values["AUTH_TOKEN"], values["CT0"]


async def search_tweets(query: str, limit: int, strict_match: bool = True) -> list[dict]:
    """Cari tweet berdasarkan keyword.

    Output mengikuti kontrak bersama RawDocument{source, text, metadata}
    (lihat root CLAUDE.md) supaya bisa langsung dikonsumsi oleh
    /backend/pipeline/integration.py tanpa branching per-source.

    X/Twitter search (bahkan tab "Latest") kadang mengembalikan tweet yang
    secara literal TIDAK mengandung kata kuncinya (semantic/related matching
    dari sistem X). strict_match=True membuang tweet yang teksnya tidak
    benar-benar memuat query, dan terus scan sampai jumlah `limit` tweet
    valid terkumpul.
    """
    auth_token, ct0 = load_env()
    cookies = f"auth_token={auth_token}; ct0={ct0}"

    api = API(str(HERE / "accounts.db"))
    accounts = await api.pool.accounts_info()
    if not any(a["active"] for a in accounts):
        await api.pool.add_account(
            username="scraper_account",
            password="placeholder",
            email="placeholder@example.com",
            email_password="placeholder",
            cookies=cookies,
        )

    query_lower = query.lower()
    max_scan = limit * 20  # batas aman biar gak scan tanpa akhir kalau keyword langka

    results = []
    scanned = 0
    async for tweet in api.search(query, limit=max_scan):
        scanned += 1
        if strict_match and query_lower not in tweet.rawContent.lower():
            continue

        results.append(
            {
                "source": "twitter",
                "text": tweet.rawContent,
                "metadata": {
                    "id": tweet.id_str,
                    "date": str(tweet.date),
                    "username": tweet.user.username,
                    "lang": tweet.lang,
                    "like_count": tweet.likeCount,
                    "retweet_count": tweet.retweetCount,
                    "reply_count": tweet.replyCount,
                    "quote_count": tweet.quoteCount,
                    "url": tweet.url,
                },
            }
        )
        if len(results) >= limit or scanned >= max_scan:
            break

    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Scrape tweet dari X/Twitter (pakai twscrape).")
    parser.add_argument("-q", "--query", default="student", help="Kata kunci pencarian")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Jumlah tweet yang diambil")
    parser.add_argument("-o", "--output", default="output.json", help="Nama file JSON output")
    args = parser.parse_args()

    results = asyncio.run(search_tweets(args.query, args.limit))

    output_path = HERE / args.output
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Selesai. {len(results)} tweet disimpan ke {output_path}")


if __name__ == "__main__":
    main()
