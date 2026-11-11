"""Stage 1: split raw Iris CSV into train/test sets."""
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

RAW = Path("data/raw/iris.csv")
OUT = Path("data/prepared")


def main():
    params = yaml.safe_load(open("params.yaml"))["prepare"]
    df = pd.read_csv(RAW)
    train, test = train_test_split(
        df,
        test_size=params["test_size"],
        random_state=params["seed"],
        stratify=df["species"],
    )
    OUT.mkdir(parents=True, exist_ok=True)
    train.to_csv(OUT / "train.csv", index=False)
    test.to_csv(OUT / "test.csv", index=False)
    print(f"train={len(train)} rows, test={len(test)} rows")


if __name__ == "__main__":
    main()
