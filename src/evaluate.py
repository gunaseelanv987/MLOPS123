"""Stage 3: evaluate the model; write metrics.json and a confusion matrix."""
import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             f1_score)

TEST = Path("data/prepared/test.csv")
MODEL = Path("models/model.pkl")


def main():
    model = joblib.load(MODEL)
    df = pd.read_csv(TEST)
    X, y = df.drop(columns="species"), df["species"]
    pred = model.predict(X)

    metrics = {
        "accuracy": round(accuracy_score(y, pred), 4),
        "f1_macro": round(f1_score(y, pred, average="macro"), 4),
    }
    Path("metrics.json").write_text(json.dumps(metrics, indent=2))

    Path("plots").mkdir(exist_ok=True)
    ConfusionMatrixDisplay.from_predictions(y, pred, cmap="Blues")
    plt.title("Confusion matrix (test set)")
    plt.savefig("plots/confusion_matrix.png", dpi=120, bbox_inches="tight")
    print(metrics)


if __name__ == "__main__":
    main()
