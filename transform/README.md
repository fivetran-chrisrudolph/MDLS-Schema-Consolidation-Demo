# Consolidation transform

Collapses the 467 `zzz_sql01_ft_scale_db_####` schemas (350 tables each,
163,450 physical tables total) landed by Fivetran into the `chris_rudolph_gcs_mdls`
destination down to 350 unified models -- one per source table name.

## How it works

`macros/get_scale_relations.sql` wraps two `dbt_utils` macros:

- `dbt_utils.get_relations_by_pattern` finds every relation across schemas
  matching `zzz_sql01_ft_scale_db_%` that contains a given table name.
- `dbt_utils.union_relations` unions those relations together and stamps
  each row with `_dbt_source_relation`, from which `source_scale_db_id`
  is extracted (which of the 467 source databases the row came from).

`models/consolidated/ft_table_####.sql` are 350 generated one-liners, each
calling `{{ consolidate_scale_table('ft_table_####') }}`. Regenerate them
with:

```bash
python3 ../scripts/generate_consolidation_models.py
```

## Running

```bash
dbt deps
dbt run --select consolidated
```

Note: `regexp_extract` in `get_scale_relations.sql` is Snowflake syntax.
Swap it for the equivalent on your destination's SQL dialect if it's not
Snowflake (e.g. Databricks/BigQuery use the same function name; DuckDB
uses `regexp_extract` too but with a different capture-group argument order).
