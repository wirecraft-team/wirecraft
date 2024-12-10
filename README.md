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

## Recommended VSCode Extensions

### Python related extensions
```
tamasfe.even-better-toml
VisualStudioExptTeam.vscodeintellicode
VisualStudioExptTeam.intellicode-api-usage-examples
ms-python.vscode-pylance
charliermarsh.ruff
ms-python.python
ms-python.debugpy
donjayamanne.python-environment-manager
christian-kohler.path-intellisense
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
