import time
from src.config import (
    TABLES,
    BASE_QUERY,
    MAX_WORKERS,
)

from src.database import create_db_engine

from src.extract import (
    load_tables_parallel,
)

from src.enrich import (
    load_dwt,
    merge_dwt,
)

from src.cleaning import clean_ais

from src.features import (
    create_trajectory_ids,
    add_motion_features,
    remove_invalid_feature_rows,
)

from src.export import (
    dataframe_to_trajectories,
    save_trajectories,
)


def main():
    total_start = time.perf_counter()
    
    engine = create_db_engine()
    
    start = time.perf_counter()
    print("Loading AIS data...", flush=True)
    df = load_tables_parallel(
        engine,
        TABLES,
        BASE_QUERY,
        MAX_WORKERS,
    )
    print(f"AIS loaded in {time.perf_counter() - start:.2f} seconds", flush=True)
    
    start = time.perf_counter()
    print("Loading DWT data...", flush=True)
    dwt_df = load_dwt(
        "../../data/concat_all_tankars_result.xlsx"
    )
    print(f"DWT loaded in {time.perf_counter() - start:.2f} seconds", flush=True)

    start = time.perf_counter()
    print("Merging DWT...", flush=True)
    df = merge_dwt(
        df,
        dwt_df,
    )
    print(f"Merge completed in {time.perf_counter() - start:.2f} seconds", flush=True)

    start = time.perf_counter()
    print("Cleaning AIS...", flush=True)
    df = clean_ais(df)
    print(f"Cleaning completed in {time.perf_counter() - start:.2f} seconds", flush=True)

    start = time.perf_counter()
    print("Creating trajectory IDs...", flush=True)
    df = create_trajectory_ids(df)
    print(f"Trajectory IDs created in {time.perf_counter() - start:.2f} seconds", flush=True)

    
    start = time.perf_counter()
    print("Creating motion features...", flush=True)
    df = add_motion_features(df)
    print(f"Motion features created in {time.perf_counter() - start:.2f} seconds", flush=True)

    start = time.perf_counter()
    print("Removing invalid rows...", flush=True)
    df = remove_invalid_feature_rows(df)
    print(f"Invalid rows removed in {time.perf_counter() - start:.2f} seconds", flush=True)

    start = time.perf_counter()
    print("Converting to trajectory format...", flush=True)
    trajectories = dataframe_to_trajectories(df)
    print(f"Conversion completed in {time.perf_counter() - start:.2f} seconds", flush=True)

    print(f"Number of trajectories: {len(trajectories):,}", flush=True)


    output_file = "trajectories_before_compression_to_use_in_github.json"
    print(f"Saving to {output_file}...", flush=True)
    
    start = time.perf_counter()
    save_trajectories(
        trajectories,
        output_file,
    )
    print(f"Saved in {time.perf_counter() - start:.2f} seconds", flush=True)
    total_time = time.perf_counter() - total_start
    print(f"\nTotal execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)", flush=True)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()