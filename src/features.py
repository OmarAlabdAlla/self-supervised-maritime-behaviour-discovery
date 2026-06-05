import pandas as pd


def create_trajectory_ids(
    df,
    hours=4,
):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values(
        ["mmsi", "timestamp"]
    )

    df["traj_id"] = (
        df.groupby("mmsi")["timestamp"]
        .transform(
            lambda x:
            (
                (x - x.min())
                .dt.total_seconds()
                // (hours * 3600)
            ).astype(int)
        )
    )

    return df


def add_motion_features(df):

    df = df.sort_values(
        ["mmsi", "traj_id", "timestamp"]
    )

    df["time_gap"] = (
        df.groupby(
            ["mmsi", "traj_id"]
        )["timestamp"]
        .diff()
        .dt.total_seconds()
        / 60
    )

    df["speed_change"] = (
        df.groupby(
            ["mmsi", "traj_id"]
        )["sog"]
        .diff()
    )

    df["turning_angle"] = (
        df.groupby(
            ["mmsi", "traj_id"]
        )["cog"]
        .diff()
    )

    df["turning_angle"] = (
        (df["turning_angle"] + 180)
        % 360
    ) - 180

    df["drift"] = (
        df["cog"]
        - df["heading"]
    )

    df["drift"] = (
        (df["drift"] + 180)
        % 360
    ) - 180

    return df


def remove_invalid_feature_rows(df):

    return df.dropna(
        subset=[
            "time_gap",
            "speed_change",
            "turning_angle",
            "drift",
        ]
    )