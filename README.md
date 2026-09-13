# Slash Command Doc Check

Scans your Lua source for `SLASH_COMMANDS["/x"] = function ...` registrations and checks that each one is documented in your ESOUI, GitHub, and Bethesda description files - catches a command you added to code but forgot to add to the docs, or a rename that only got fixed in one place.

Alias registrations (`SLASH_COMMANDS["/x"] = SLASH_COMMANDS["/y"]`) are automatically excluded - these are intentional shortcuts, not meant to be individually documented, and including them would produce constant false positives.

## Usage

```yaml
name: Slash Command Doc Check

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: MPHONlC/slash-command-doc-check@Version-0.0.1
```

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `source_glob` | No | `**/*.lua` | Recursive glob matching your Lua source. |
| `esoui_file` | No | `README_ESOUI.txt` | ESOUI (BBCode) description file. |
| `github_file` | No | `README.md` | GitHub-flavored markdown description file. |
| `bethesda_file` | No | `README_BETHESDA.txt` | Bethesda (plain markdown) description file. |

## License

MIT - see [LICENSE](LICENSE).
