import json
import time

from src.compression import (
    compress_dp_all,
    compression_stats,
)

INPUT_FILE = (
    "trajectories_before_compression_to_use_in_github.json"
)

OUTPUT_FILE = (
    "trajectories_after_compression_50m_to_use_in_github.json"
)


def main():

    start = time.perf_counter()

    print(
        "Loading trajectories...",
        flush=True,
    )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    trajectories = data["trajectories"]

    print(
        f"Loaded {len(trajectories):,} trajectories",
        flush=True,
    )

    compressed = compress_dp_all(
        trajectories,
        epsilon=50,
        workers=32,
    )

    compression_stats(
        trajectories,
        compressed,
    )

    output = {
        "num_trajectories": len(
            compressed
        ),
        "total_points": sum(
            len(t)
            for t in compressed
        ),
        "trajectories": compressed,
    }

    print(
        "Saving compressed file...",
        flush=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            default=str,
        )

    print(
        f"Done in "
        f"{time.perf_counter() - start:.2f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()