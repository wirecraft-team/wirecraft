# Wirecraft

The Wirecraft project!

## Installation instructions

The project is divided into two parts: Godot for the client, python for the server.

### Install the client

(#TODO) Download the distributed build in the release section at https://github.com/wirecraft-team/wirecraft/releases

### Install the server

> [!IMPORTANT]
> The project requires Python >= 3.12 ! (If you use `uv` or Docker, python version isn't an issue).

#### Install from git

> [!NOTE]
> To install the project at a specific version, you can specify a commit ID / a tag name / a branch.  
> Replace `@main` by `@ee0d809` or `@vx.x.x` or `@branch` in the URL.

Using pip:
```bash
pip install git+https://github.com/wirecraft-team/wirecraft.git@main#subdirectory=python -U
wirecraft-server
```

Using uvx:
```bash
uvx --from uvx --from git+https://github.com/wirecraft-team/wirecraft.git@main#subdirectory=python wirecraft-server
```

Using pipx: should be possible.

#### Install from sources

Clone the repo / download a zip.

Using uv:
```bash
cd python
uv sync --no-dev
uv run wirecraft-server
```
nb: `uv run wirecraft-server` install dev deps, I don't know why. (#TODO)  
Instead of using `uv run`, you can also activate the venv at `.venv` and run `wirecraft-server`.

Using pip:
```bash
cd python
python -m venv venv
source venv/bin/activate
pip install .
wirecraft-server
```

#### Install with Docker

#TODO (soon)

### Debug options

- `show_center`: add a red square at position 0,0 in the map

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

If you are no a big fan of `print("a")`, `print("aa")`, `print("aaaaaaaaaaaaaaaa")`, you can use the VSCode Debugger! (Or any other debugger, but I will only give explanations for VSCode).

> [!NOTE]
> The following instructions will work, but I'm not sure if it is the best way to proceed, because it doesn't launch the script in the same way than using `uv run wirecraft`.  
> However, it works, so be happy with that.

Create a `.vscode/launch.json` and add the following config:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Wirecraft",
            "type": "debugpy",
            "request": "launch",
            "program": "src/client/__main__.py",
            "console": "integratedTerminal"
        }
    ]
}
```

Then, on the debugger tab, you can do `Debug Wirecraft`! Your program will stop on breakpoints, giving you the ability to see your variables, etc...


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
