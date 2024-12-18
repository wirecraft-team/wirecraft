# WireCraft

The WireCraft project!

## Installation instructions

> [!IMPORTANT]
> The project requires Python >= 3.12 !

> [!WARNING]
> This installation method doesn't work for now.

```bash
pip install git+https://github.com/wirecraft-team/wirecraft.git -U
wirecraft
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
