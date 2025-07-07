# Wirecraft

The Wirecraft project!

This project is a school project and is part of our studies. It isn't intended for public use at the moment, but you can give it a try if you want.
It's a network simulation game, where the aim is to carry out various requested tasks (getting devices to communicate with each other, supporting a load of requests, setting up load balancing, etc... it's not a "client" of an existing game but an entire game).

## Installation instructions

The project is divided into two parts: Godot for the client, python for the server.

### Install the client

Download the distributed build in the release section at https://github.com/wirecraft-team/wirecraft/releases  
You can also get the latest builds from CI/CD artifacts at https://github.com/wirecraft-team/wirecraft/actions/workflows/godot-build.yml

#### Windows:
1. Run wirecraft.exe

#### Linux:
1. `chmod +x wirecraftx86_64`
2. `./wirecraftx86_64`

#### MacOs:
1. Extract wirecraft.zip
2. Run the .app
3. Your system will say that the app can't be opened, and you should move it to bin. DON'T DO THIS 😭
4. Go to your System Settings -> Privacy & Security -> Security -> "Open Anyway"
99. Buy us a certificate

### Install the server

> [!IMPORTANT]
> The project requires Python >= 3.12 ! (If you use `uv` or Docker, python version isn't an issue).

Wirecraft server is a Python package. The options are available with the `--help` command.  
You have plenty options to install & launch it, depending on whatever you prefer. Here are some instructions example, but fill free to use your favorite way.

#### Install the package

##### Directly from git

You can install if from the git repo, for example:
```bash
pip install git+https://github.com/wirecraft-team/wirecraft.git@main#subdirectory=python -U
```
Then run it with `wirecraft-server` CLI.

Or install & run it directly with tools like `uvx` or `pipx`, for example:
```bash
uvx --from uvx --from git+https://github.com/wirecraft-team/wirecraft.git@main#subdirectory=python wirecraft-server
```

> [!NOTE]
> To install the project at a specific version, you can specify a commit ID / a tag name / a branch.  
> Replace `@main` with `@ee0d809` or `@vx.x.x` or `@branch` in the URL.

##### From sources

You can clone the repo, enter the `python directory`, and install from local directory, for example with `pip install .`.  
You can also directly use `uv run wirecraft-server`.

#### Using docker & compose

A Dockerfile & a docker-compose.yaml is available to launch directly the server using PostgreSQL as a backend database.

`compose.yaml` is available at `python/compose.yaml`. Sources needs to be present to build is correctly.

```bash
git clone https://github.com/wirecraft-team/wirecraft.git@main
cd wirecraft/python
docker compose up
```

## Development instructions

### Install `uv`

Check https://docs.astral.sh/uv/getting-started/installation/

### Install the dependencies and developer tools

```bash
uv sync --dev
```

### Run the project

```bash
uv run wirecraft
```

### Run the linting etc.. **before you commit** !

```bash
uv run tox
```

### Init pre-commit

```bash
pre-commit install
```

### (Optional) Activate the virtual environment (to have access to all the tools, dependencies...)

> [!NOTE]
> `uv sync` will create a virtual environment under a `.venv` directory.
> When you use the command `uv run {command}`, `uv` will automatically call your command from your virtual environment, so you don't need to activate it.
> For example, before enable to virtual environment, you can do `uv run tox`, `uv run wirecraft`, `uv run ruff`...
> But after you enable it, you can directly do `tox`, `wirecraft`, `ruff`...

#### Linux / MacOS
```bash
source .venv/bin/activate
```

#### Windows
```bash
./.venv/Scripts/activate.bat
```

### Debugging

### Debug options

You can add debugs options (that will add prints, etc...) for the server. Add parameters to the command with `--debug`. For example, `wirecraft-server --debug A --debug B`.

The following debug options are available:
- nones.

### Log level

You can increase the log level for the server using `--log-level`. Log levels are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `NOTSET`.

### Database

Whenever you made an edit to the database layout, generate a new revision.  
This can be achieved with the following commands:

```bash
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "message"
```

We first create an SQLite database locally and apply the last version declared by alembic with the `upgrade` command, then we create a new revision. `--autogenerate` will compares the **current state** of the database (we just created) and the declared model from the code.

## Recommended VSCode Extensions

### Python related extensions

#### Important ones (for the project)
```
ms-python.vscode-pylance
ms-python.python
ms-python.debugpy
charliermarsh.ruff
```

#### Bonus ones
```
christian-kohler.path-intellisense
VisualStudioExptTeam.vscodeintellicode
VisualStudioExptTeam.intellicode-api-usage-examples
donjayamanne.python-environment-manager
tamasfe.even-better-toml
```

### General extensions that are usefull
```
bierner.emojisense
aaron-bond.better-comments
alefragnani.project-manager
alefragnani.Bookmarks
streetsidesoftware.code-spell-checker
adpyke.codesnap
usernamehw.errorlens
TTOOWA.in-your-face-incredible
IBM.output-colorizer
johnpapa.vscode-peacock
Gruntfuggly.todo-tree
PeterSchmalfeldt.explorer-exclude
streetsidesoftware.code-spell-checker-french
```

### Git related extensions
```
eamodio.gitlens
GitHub.remotehub
GitHub.vscode-pull-request-github
github.vscode-github-actions
donjayamanne.githistory
```

### Markdown related extensions (bonus)
```
bierner.markdown-preview-github-styles
bierner.markdown-mermaid
bierner.markdown-checkbox
bierner.markdown-yaml-preamble
bierner.markdown-footnotes
darkriszty.markdown-table-prettify
bpruitt-goddard.mermaid-markdown-syntax-highlighting
```

## Recommended VSCode Settings

Use the command `>Preferences: Open user Settings (JSON)` (using `CTRL+P`).  
(You can also use the command `>Preferences: Open Workspace Settings (JSON)` if you don't want to edit your global settings).

Paste the following settings:
```json
{
    "[python]": {
      "editor.rulers": [
        120
      ],
      "editor.formatOnSave": true,
      "editor.defaultFormatter": "charliermarsh.ruff"
    },
    "python.languageServer": "Pylance",
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.completeFunctionParens": false,
    "autoDocstring.docstringFormat": "google-notypes",
    "autoDocstring.startOnNewLine": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.terminal.activateEnvironment": true,
}
```
