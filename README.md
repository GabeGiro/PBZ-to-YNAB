# PBZ-to-YNAB

## Instal virtual environment

Recommended python version: 3.12

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Ignore Jupyter Notebook output
To ignore the output of Jupyter Notebooks use the following steps:

1. Install `nbstripout`:
   ```bash
   pip install nbstripout
   ```
2. Initialize `nbstripout` in your repository:
   ```bash
   nbstripout --install
   ```