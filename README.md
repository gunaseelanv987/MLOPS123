# Iris MLOps lab (Git + DVC + DagsHub + CML)

This project trains a Random Forest classifier on Iris. Git versions code, parameters, and DVC metadata; DVC versions the dataset and pipeline outputs; DagsHub hosts the DVC remote; and GitHub Actions uses CML to post experiment comparisons on pull requests.

## 1. Set up the environment

Run from the project root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that window, then activate the environment again.

## 2. Run the notebook and report metrics

```powershell
jupyter notebook notebooks/iris_baseline.ipynb
```

The baseline uses a stratified 80/20 split and a 100-tree Random Forest with maximum depth 5. The pipeline baseline reports accuracy **0.9333** and macro F1 **0.9333** in `metrics.json`.

## 3. Track the dataset with DVC and configure DagsHub

This checkout has DVC initialized, the `origin` DagsHub remote configured, and the CSV tracked in `data/raw/iris.csv.dvc`. The remote URL is `https://dagshub.com/gunaseelanv987/MLOPS123.dvc`.

To reproduce the one-time setup in a new repository:

```powershell
dvc init
dvc remote add -d origin https://dagshub.com/gunaseelanv987/MLOPS123.dvc
dvc add data/raw/iris.csv
```

Authenticate locally without committing a token. Create a DagsHub access token with repository read/write permission, then set the credentials in the ignored local DVC config:

```powershell
dvc remote modify --local origin auth basic
dvc remote modify --local origin user YOUR_DAGSHUB_USERNAME
dvc remote modify --local origin password YOUR_DAGSHUB_TOKEN
dvc push
```

Keep the token private. Do not commit `.dvc/config.local` or share its contents. On a fresh clone, authenticate the same way and run `dvc pull` to fetch the tracked dataset.

Commit the DVC metadata and project files, not the ignored dataset contents. DVC generated `data/.gitignore` and `models/.gitignore` for pipeline outputs; include them:

```powershell
git add .dvc .dvcignore .gitignore data/raw/iris.csv.dvc data/raw/.gitignore data/.gitignore models/.gitignore
git add src params.yaml dvc.yaml requirements.txt notebooks .github README.md
git add dvc.lock metrics.json plots
git commit -m "Add DVC Iris pipeline"
git push
```

## 4. Reproduce the pipeline and compare an experiment

```powershell
dvc repro
dvc dag
git add dvc.lock metrics.json plots
git commit -m "Record baseline experiment"
git tag baseline
```

Change `train.max_depth` in `params.yaml` (for example, from `5` to `2`) and rerun:

```powershell
dvc repro
dvc params diff baseline
dvc metrics diff baseline
```

Commit the new experiment so its parameters, lockfile, metrics, and plot can be compared later:

```powershell
git add params.yaml dvc.lock metrics.json plots
git commit -m "Compare shallower Iris model"
```

## 5. GitHub Actions and CML pull-request reports

In the GitHub repository that mirrors the DagsHub project, add these Actions repository secrets:

- `DAGSHUB_USER`: your DagsHub username.
- `DAGSHUB_TOKEN`: a DagsHub access token with read access to the DVC remote.

The workflow uses `GITHUB_TOKEN` to publish a CML comment; the workflow grants it pull-request write permission. Push the `main` branch and open a pull request against `main`. The action installs dependencies, authenticates to DagsHub, runs `dvc pull` and `dvc repro`, compares metrics and parameters with `main`, and posts the report.

The DagsHub remote stores DVC data; it is separate from the Git remote used to push branches and pull requests.
