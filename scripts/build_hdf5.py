import json
import time

from src.image_generation import (
    trajectories_to_hdf5,
    count_hdf5_datasets,
)


INPUT_FILE = "trajectories_after_compression_50m_to_use_in_github.json"

OUTPUT_FILE = "DP_50_Compressed_allaData_3ports_to_use_in_github.hdf5"

WORKERS = 16


def main():

    start = time.perf_counter()

    print(
        "Loading compressed trajectories...",
        flush=True,
    )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    compressed_trajectories = data["trajectories"]

    print(
        f"Total trajectories: {len(compressed_trajectories):,}",
        flush=True,
    )

    saved_count = trajectories_to_hdf5(
        compressed_trajectories,
        OUTPUT_FILE,
        workers=WORKERS,
    )

    dataset_count = count_hdf5_datasets(
        OUTPUT_FILE
    )

    print(
        f"Total trajectories: {len(compressed_trajectories):,}",
        flush=True,
    )

    print(
        f"Saved trajectories: {saved_count:,}",
        flush=True,
    )

    print(
        f"Datasets in file: {dataset_count:,}",
        flush=True,
    )

    total_time = time.perf_counter() - start

    print(
        f"Done in {total_time:.2f} seconds "
        f"({total_time / 60:.2f} minutes)",
        flush=True,
    )


if __name__ == "__main__":
    main()