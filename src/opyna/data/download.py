"""Descarga en streaming de Amazon Reviews 2023 y muestreo estratificado.

El dataset completo es enorme, así que se lee en streaming desde Hugging Face
y se toma una muestra equilibrada por rating (1-5 estrellas). El resultado se
guarda como parquet en ``data/processed``.

Uso:
    python -m opyna.data.download --category Electronics --n-per-rating 5000

Nota: verifica el nombre exacto de la config en la web del dataset
(McAuley-Lab/Amazon-Reviews-2023). Para reseñas suele ser
``raw_review_<Categoria>``.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import pandas as pd
from datasets import load_dataset  # requiere datasets<4 (loading script)
from tqdm import tqdm

from opyna.settings import settings

DATASET = "McAuley-Lab/Amazon-Reviews-2023"
KEEP_COLS = ["rating", "title", "text", "asin", "parent_asin", "timestamp",
             "helpful_vote", "verified_purchase"]


def download_sample(category: str = "Electronics", n_per_rating: int = 5000) -> pd.DataFrame:
    """Devuelve una muestra estratificada por rating (1..5)."""
    config = f"raw_review_{category}"
    stream = load_dataset(DATASET, config, split="full",
                          streaming=True, trust_remote_code=True)

    buckets: dict[int, list[dict]] = defaultdict(list)
    target_total = n_per_rating * 5
    pbar = tqdm(total=target_total, desc=f"Muestreando {category}")

    for row in stream:
        r = int(row.get("rating", 0))
        if r < 1 or r > 5:
            continue
        if len(buckets[r]) >= n_per_rating:
            if all(len(buckets[k]) >= n_per_rating for k in range(1, 6)):
                break
            continue
        buckets[r].append({c: row.get(c) for c in KEEP_COLS})
        pbar.update(1)
    pbar.close()

    df = pd.DataFrame([row for rows in buckets.values() for row in rows])
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default="Electronics")
    ap.add_argument("--n-per-rating", type=int, default=5000)
    args = ap.parse_args()

    df = download_sample(args.category, args.n_per_rating)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    out = settings.processed_dir / f"reviews_{args.category.lower()}.parquet"
    df.to_parquet(out, index=False)
    print(f"Guardado {len(df):,} reseñas en {out}")
    print(df["rating"].value_counts().sort_index())


if __name__ == "__main__":
    main()
