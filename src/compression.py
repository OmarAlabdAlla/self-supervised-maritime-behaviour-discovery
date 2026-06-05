import numpy as np
import time
from multiprocessing import Pool
from tqdm import tqdm

EARTH_RADIUS = 6371000


def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(
        np.radians,
        [lon1, lat1, lon2, lat2]
    )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return EARTH_RADIUS * c


def perpendicular_distance(
    point,
    start,
    end,
):

    lon0, lat0 = point
    lon1, lat1 = start
    lon2, lat2 = end

    if (lon1 == lon2) and (lat1 == lat2):
        return haversine(
            lon0,
            lat0,
            lon1,
            lat1,
        )

    lon0, lat0, lon1, lat1, lon2, lat2 = map(
        np.radians,
        [
            lon0,
            lat0,
            lon1,
            lat1,
            lon2,
            lat2,
        ],
    )

    x0 = np.cos(lat0) * np.cos(lon0)
    y0 = np.cos(lat0) * np.sin(lon0)

    x1 = np.cos(lat1) * np.cos(lon1)
    y1 = np.cos(lat1) * np.sin(lon1)

    x2 = np.cos(lat2) * np.cos(lon2)
    y2 = np.cos(lat2) * np.sin(lon2)

    num = abs(
        (y2 - y1) * x0
        - (x2 - x1) * y0
        + x2 * y1
        - y2 * x1
    )

    den = np.sqrt(
        (y2 - y1) ** 2
        + (x2 - x1) ** 2
    )

    return EARTH_RADIUS * num / den


def douglas_peucker(
    points,
    epsilon,
):

    if len(points) < 3:
        return points

    start = points[0]
    end = points[-1]

    lons = np.array(
        [p["lon"] for p in points]
    )

    lats = np.array(
        [p["lat"] for p in points]
    )

    dists = []

    for i in range(1, len(points) - 1):

        d = perpendicular_distance(
            (lons[i], lats[i]),
            (
                start["lon"],
                start["lat"],
            ),
            (
                end["lon"],
                end["lat"],
            ),
        )

        dists.append(d)

    dists = np.array(dists)

    max_index = np.argmax(dists)
    max_dist = dists[max_index]

    if max_dist > epsilon:

        split = max_index + 1

        left = douglas_peucker(
            points[: split + 1],
            epsilon,
        )

        right = douglas_peucker(
            points[split:],
            epsilon,
        )

        return left[:-1] + right

    return [start, end]


def _worker(args):

    traj, epsilon = args

    return douglas_peucker(
        traj,
        epsilon,
    )


def compress_dp_all(
    trajectories,
    epsilon=50,
    workers=32,
):

    start_time = time.time()

    print(
        f"Compressing {len(trajectories):,} trajectories...",
        flush=True,
    )

    with Pool(workers) as pool:

        compressed = list(
            tqdm(
                pool.imap(
                    _worker,
                    [
                        (traj, epsilon)
                        for traj in trajectories
                    ],
                    chunksize=50,
                ),
                total=len(trajectories),
            )
        )

    print(
        f"Compression finished in "
        f"{time.time() - start_time:.2f}s",
        flush=True,
    )

    return compressed


def compression_stats(
    original,
    compressed,
):

    original_points = sum(
        len(t)
        for t in original
    )

    compressed_points = sum(
        len(t)
        for t in compressed
    )

    removed = (
        original_points
        - compressed_points
    )

    compression_rate = (
        removed
        / original_points
    )

    print(
        f"Original points: {original_points:,}"
    )

    print(
        f"Compressed points: {compressed_points:,}"
    )

    print(
        f"Removed points: {removed:,}"
    )

    print(
        f"Compression rate: "
        f"{compression_rate:.4f}"
    )