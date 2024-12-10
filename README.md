# client
The client side of WireCraft.


## Commands

### Install `uv`

Check https://docs.astral.sh/uv/getting-started/installation/

### Install the project (dependencies...)

```bash
uv sync
```

### Run the project

```bash
uv run python ./src/main.py
```

### Run the linting etc.. **before you commit** !

```bash
uv run tox
```

### (Optional) Activate the virtual environment (to have access to all the tools, dependencies...)

#### Linux / MacOS
```bash
source .venv/bin/activate
```

#### Windows
```bash
./.venv/Scripts/activate.bat
```
