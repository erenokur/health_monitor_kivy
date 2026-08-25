# Heath Monitor Kivy

This project is a small Kivy desktop app that tracks user blood pressure and medicine.

## Requirements

- Python 3.12.3
- pip

## Install

Create or activate the virtual environment, then install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you are using this workspace's existing virtualenv:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Start the app with:

```bash
python main.py
```

Or with the workspace virtualenv directly:

```bash
.venv/bin/python main.py
```

## Files

- `main.py`: Kivy application entrypoint
- `holiday_manager.py`: holiday add/list/delete screen for `tatiller.json`
- `servis_settings.json`: persisted app settings
- `tatiller.json`: holiday definitions used in the calculation
