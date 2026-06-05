import json


COLS = [
    "traj_id",
    "imo",
    "ship_name",
    "mmsi",
    "time",
    "lon",
    "lat",
    "sog",
    "cog",
    "nav",
    "time_gap",
    "speed_change",
    "turning_angle",
    "drift",
]


def dataframe_to_trajectories(df):

    df = df.rename(
        columns={
            "timestamp": "time",
            "nav_status": "nav",
        }
    )

    df["time"] = (
        df["time"]
        .dt.strftime("%Y-%m-%dT%H:%M:%S")
    )

    trajectories = [
        group[COLS].to_dict("records")
        for _, group in df.groupby(
            ["mmsi", "traj_id"],
            sort=False,
        )
    ]

    trajectories = [
        traj
        for traj in trajectories
        if len(traj) > 1
    ]

    return trajectories


def save_trajectories(
    trajectories,
    output_file,
):

    data = {
        "num_trajectories": len(
            trajectories
        ),
        "total_points": sum(
            len(t)
            for t in trajectories
        ),
        "trajectories": trajectories,
    }

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            default=str,
            indent=2,
        )