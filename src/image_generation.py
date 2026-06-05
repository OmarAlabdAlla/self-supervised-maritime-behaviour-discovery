import h5py
import numpy as np
import pandas as pd
import geopandas as gpd

from multiprocessing import Pool
from tqdm import tqdm
from shapely.geometry import Point, LineString, box
from rasterio.features import rasterize
from rasterio.transform import Affine, from_bounds


def get_segmented_value_trace(
    dataf: gpd.GeoDataFrame,
    value_column: str,
    resolution: int,
    transform: Affine,
    dtype: np.dtype,
) -> np.ndarray:

    line_value_pairs = []
    geom_coords = dataf.geometry

    for i in range(1, dataf.shape[0]):
        segment = LineString(
            [
                geom_coords.iloc[i - 1],
                geom_coords.iloc[i],
            ]
        )

        value = dataf[value_column].iloc[i]

        line_value_pairs.append(
            (segment, value)
        )

    image = rasterize(
        line_value_pairs,
        out_shape=(resolution, resolution),
        transform=transform,
        dtype=dtype,
    )

    return np.expand_dims(image, axis=0)


def voyage_array_from_points(
    data: gpd.GeoDataFrame,
    coastlines=None,
    resolution: int = 256,
    dtype: np.dtype = np.float32,
    value_cols=None,
):

    if coastlines is None:
        coastlines = []

    minx, miny, maxx, maxy = data.total_bounds

    center = box(
        minx,
        miny,
        maxx,
        maxy,
    ).centroid

    diagonal = max(
        (maxy - miny) / 2,
        (maxx - minx) / 2,
        5.0 * 90 / 10_000.0,
    )

    square_box = Point(center).buffer(
        diagonal,
        cap_style=3,
    )

    square_box = gpd.GeoDataFrame(
        [{"geometry": square_box}],
        crs="EPSG:4326",
    )

    transform = from_bounds(
        *square_box.total_bounds,
        resolution,
        resolution,
    )

    travel_line = gpd.GeoDataFrame(
        [
            {
                "geometry": LineString(
                    data.geometry
                )
            }
        ],
        crs="EPSG:4326",
    )

    image = rasterize(
        travel_line.geometry,
        out_shape=(resolution, resolution),
        transform=transform,
        dtype=dtype,
    )

    image = np.expand_dims(
        image,
        axis=0,
    )

    if value_cols is None:
        value_cols = []

    if isinstance(value_cols, str):
        value_cols = [value_cols]

    for value_column in value_cols:

        extra_layer = get_segmented_value_trace(
            dataf=data,
            value_column=value_column,
            resolution=resolution,
            transform=transform,
            dtype=dtype,
        )

        image = np.concatenate(
            [image, extra_layer],
            axis=0,
        )

    for coastline in coastlines:

        try:
            coastline = coastline.overlay(
                square_box,
                how="intersection",
            )

            coast_raster = rasterize(
                coastline.geometry.boundary,
                out_shape=(resolution, resolution),
                transform=transform,
                dtype=dtype,
            )

            image = np.concatenate(
                [
                    image,
                    np.expand_dims(
                        coast_raster,
                        axis=0,
                    ),
                ],
                axis=0,
            )

        except ValueError:

            image = np.concatenate(
                [
                    image,
                    np.zeros(
                        (
                            1,
                            resolution,
                            resolution,
                        ),
                        dtype=dtype,
                    ),
                ],
                axis=0,
            )

    return image


def process_traj(args):

    i, traj = args

    if len(traj) <= 2:
        return None

    df = pd.DataFrame(traj)

    df["geometry"] = [
        Point(lon, lat)
        for lon, lat in zip(
            df["lon"],
            df["lat"],
        )
    ]

    gdf = gpd.GeoDataFrame(
        df,
        geometry="geometry",
        crs="EPSG:4326",
    )

    gdf = gdf.set_index("time")

    image = voyage_array_from_points(
        gdf,
        coastlines=[],
        resolution=256,
        value_cols=[
            "drift",
            "turning_angle",
            "speed_change",
        ],
    )

    return {
        "i": i,
        "imo": str(gdf["imo"].iloc[0]),
        "mmsi": str(gdf["mmsi"].iloc[0]),
        "ship_name": str(gdf["ship_name"].iloc[0]),
        "start_time": str(gdf.index.min()),
        "end_time": str(gdf.index.max()),
        "length": len(gdf),
        "coords": np.array(
            [
                (p.x, p.y)
                for p in gdf.geometry
            ],
            dtype=np.float32,
        ),
        "timestamps": np.array(
            [
                str(t)
                for t in gdf.index
            ],
            dtype="S32",
        ),
        "image": image,
    }


def trajectories_to_hdf5(
    trajectories,
    output_file,
    workers=16,
):

    print(
        f"Creating images for {len(trajectories):,} trajectories...",
        flush=True,
    )

    with Pool(workers) as pool:

        results = list(
            tqdm(
                pool.imap(
                    process_traj,
                    enumerate(trajectories),
                    chunksize=20,
                ),
                total=len(trajectories),
            )
        )

    results = [
        r for r in results
        if r is not None
    ]

    print(
        f"Saving {len(results):,} trajectories to HDF5...",
        flush=True,
    )

    with h5py.File(output_file, "w") as file:

        for r in results:

            name = (
                f"traj_{r['i']}_imo_{r['imo']}"
            )

            dset = file.create_dataset(
                name,
                data=r["image"],
            )

            dset.attrs["length"] = r["length"]
            dset.attrs["mmsi"] = r["mmsi"]
            dset.attrs["ship_name"] = r["ship_name"]
            dset.attrs["start_time"] = r["start_time"]
            dset.attrs["end_time"] = r["end_time"]
            dset.attrs["coords"] = r["coords"]
            dset.attrs["timestamps"] = r["timestamps"]

    print(
        f"HDF5 saved to {output_file}",
        flush=True,
    )

    return len(results)


def count_hdf5_datasets(hdf5_file):

    with h5py.File(hdf5_file, "r") as f:
        return len(f)