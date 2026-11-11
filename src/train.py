"""Stage 2: train a Random Forest on the prepared training set."""
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestClassifier

TRAIN = Path("data/prepared/train.csv")
MODEL = Path("models/model.pkl")


def main():
    params = yaml.safe_load(open("params.yaml"))["train"]
    df = pd.read_csv(TRAIN)
    X, y = df.drop(columns="species"), df["species"]

    model = RandomForestClassifier(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        random_state=params["seed"],
    )
    model.fit(X, y)

    MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL)
    print(f"model saved to {MODEL}")


if __name__ == "__main__":
    main()
