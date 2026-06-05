import os
import random

import h5py
import numpy as np
import matplotlib.pyplot as plt


HDF5_FILE = (
    "DP_50_Compressed_allaData_3ports_to_use_in_github.hdf5"
)

PLOTS_DIR = "plots"


def plot_all_channels(
    data,
    title="",
    save_path=None,
):

    titles = [
        "Trajectory",
        "Drift",
        "Turning Angle",
        "Speed Change",
    ]

    fig, axes = plt.subplots(
        1,
        4,
        figsize=(18, 4),
    )

    for i in range(4):

        ax = axes[i]

        im = ax.imshow(data[i])

        ax.set_title(titles[i])

        ax.axis("off")

        plt.colorbar(
            im,
            ax=ax,
        )

    plt.suptitle(title)

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            bbox_inches="tight",
        )

    plt.close()


def plot_overlay(
    data,
    channel=1,
    title="Overlay",
    save_path=None,
):

    plt.figure(figsize=(6, 6))

    plt.imshow(
        data[0],
        cmap="gray",
    )

    plt.imshow(
        data[channel],
        cmap="jet",
        alpha=0.6,
    )

    plt.title(title)

    plt.axis("off")

    plt.colorbar()

    if save_path:
        plt.savefig(
            save_path,
            bbox_inches="tight",
        )

    plt.close()


def show_summary(hdf5_file):

    with h5py.File(hdf5_file, "r") as f:

        keys = list(f.keys())

        print(
            "Datasets:",
            keys[:5],
            flush=True,
        )

        print(
            "Number of trajectories:",
            len(keys),
            flush=True,
        )

        sample_key = keys[0]

        sample = f[sample_key][:]

        print(
            "\nSample key:",
            sample_key,
            flush=True,
        )

        print(
            "Min/Max:",
            sample.min(),
            sample.max(),
            flush=True,
        )

        print(
            "Shape:",
            sample.shape,
            flush=True,
        )

        print(
            "Dtype:",
            sample.dtype,
            flush=True,
        )

    return keys


def plot_first_sample(
    hdf5_file,
    keys,
):

    with h5py.File(hdf5_file, "r") as f:

        key = keys[0]

        data = f[key][:]

    plot_all_channels(
        data,
        title=key,
        save_path=f"{PLOTS_DIR}/first_sample.png",
    )

    plot_overlay(
        data,
        channel=1,
        title=f"{key} - Drift",
        save_path=f"{PLOTS_DIR}/first_sample_overlay.png",
    )

    print(
        "Saved first sample plots",
        flush=True,
    )


def plot_random_samples(
    hdf5_file,
    keys,
    n_samples=5,
):

    with h5py.File(hdf5_file, "r") as f:

        random_keys = random.sample(
            keys,
            n_samples,
        )

        for idx, key in enumerate(random_keys):

            data = f[key][:]

            plot_all_channels(
                data,
                title=key,
                save_path=f"{PLOTS_DIR}/random_{idx+1}.png",
            )

    print(
        f"Saved {n_samples} random samples",
        flush=True,
    )


def plot_feature_histograms(
    hdf5_file,
    keys,
):

    all_drift = []
    all_turn = []
    all_speed = []

    with h5py.File(hdf5_file, "r") as f:

        for key in keys:

            data = f[key][:]

            mask = data[0] > 0

            if np.any(mask):

                all_drift.append(
                    data[1][mask]
                )

                all_turn.append(
                    data[2][mask]
                )

                all_speed.append(
                    data[3][mask]
                )

    all_drift = np.concatenate(
        all_drift
    )

    all_turn = np.concatenate(
        all_turn
    )

    all_speed = np.concatenate(
        all_speed
    )

    plt.figure(
        figsize=(15, 4)
    )

    plt.subplot(1, 3, 1)

    plt.hist(
        all_drift,
        bins=100,
    )

    plt.title(
        "Drift (trajectory only)"
    )

    plt.subplot(1, 3, 2)

    plt.hist(
        all_turn,
        bins=100,
    )

    plt.title(
        "Turning Angle (trajectory only)"
    )

    plt.subplot(1, 3, 3)

    plt.hist(
        all_speed,
        bins=100,
    )

    plt.title(
        "Speed Change (trajectory only)"
    )

    plt.tight_layout()

    plt.savefig(
        f"{PLOTS_DIR}/feature_histograms.png",
        bbox_inches="tight",
    )

    plt.close()

    print(
        "\nStats (trajectory pixels only):",
        flush=True,
    )

    print(
        "Drift:",
        np.min(all_drift),
        np.max(all_drift),
        np.mean(all_drift),
        np.std(all_drift),
        flush=True,
    )

    print(
        "Turning:",
        np.min(all_turn),
        np.max(all_turn),
        np.mean(all_turn),
        np.std(all_turn),
        flush=True,
    )

    print(
        "Speed change:",
        np.min(all_speed),
        np.max(all_speed),
        np.mean(all_speed),
        np.std(all_speed),
        flush=True,
    )

    print(
        "\nSaved histogram plot",
        flush=True,
    )


def main():

    os.makedirs(
        PLOTS_DIR,
        exist_ok=True,
    )

    keys = show_summary(
        HDF5_FILE
    )

    plot_first_sample(
        HDF5_FILE,
        keys,
    )

    plot_random_samples(
        HDF5_FILE,
        keys,
        n_samples=5,
    )

    plot_feature_histograms(
        HDF5_FILE,
        keys,
    )

    print(
        f"\nPlots saved to '{PLOTS_DIR}/'",
        flush=True,
    )


if __name__ == "__main__":
    main()