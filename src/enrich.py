import pandas as pd


def load_dwt(filepath):

    dwt_df = pd.read_excel(
        filepath,
        dtype={"imo": str},
    )

    dwt_df = dwt_df.rename(
        columns={
            "Deadweight": "dwt"
        }
    )

    return dwt_df[["imo", "dwt"]]


def merge_dwt(df, dwt_df):

    return df.merge(
        dwt_df,
        on="imo",
        how="left",
    )