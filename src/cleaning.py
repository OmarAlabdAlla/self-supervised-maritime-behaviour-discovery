def clean_ais(df):

    df = df[df["sog"] <= 40]

    df = df[df["cog"] <= 360]
    df = df[df["heading"] <= 360]

    df = df[df["dwt"].notna()]

    df = df[df["dwt"] > 1000]

    return df