# WireCraft

The WireCraft project!

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
