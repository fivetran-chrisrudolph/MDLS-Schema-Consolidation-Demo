#!/usr/bin/env python3
"""Generate one dbt model per source table name, each unioning that table
across all 467 zzz_sql01_ft_scale_db_#### schemas via consolidate_scale_table().

Collapses 467 schemas x 350 tables (163,450 physical tables) into 350 models.
Re-run any time the source table count changes -- it's idempotent.
"""
import os

TABLE_COUNT = 350
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "transform", "models", "consolidated",
)

MODEL_TEMPLATE = "{{{{ consolidate_scale_table('ft_table_{n:04d}') }}}}\n"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    written = 0
    for n in range(1, TABLE_COUNT + 1):
        path = os.path.join(OUTPUT_DIR, f"ft_table_{n:04d}.sql")
        with open(path, "w") as f:
            f.write(MODEL_TEMPLATE.format(n=n))
        written += 1
    print(f"Wrote {written} consolidation models to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
