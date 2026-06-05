import pandas as pd

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)


def query_table(engine, table, base_query):

    query = base_query.format(table=table)

    try:

        with engine.connect() as conn:
            df = pd.read_sql(query, conn)

        print(f"{table}: {len(df):,} rows")
        return df

    except Exception as e:

        print(f"{table}: skipped ({e})")
        return None


def load_tables_parallel(
    engine,
    tables,
    base_query,
    max_workers=8,
):

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = {
            executor.submit(
                query_table,
                engine,
                table,
                base_query,
            ): table
            for table in tables
        }

        parts = [
            future.result()
            for future in as_completed(futures)
        ]

    parts = [
        p for p in parts
        if p is not None and not p.empty
    ]

    return pd.concat(
        parts,
        ignore_index=True,
    )