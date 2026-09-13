# ESO Addon Slash Command Doc Check

Scans your ESO addon's Lua source for `SLASH_COMMANDS["/x"] = function ...` registrations (ESO's own slash-command API - other Lua-addon games use a different convention, e.g. WoW's `SlashCmdList`) and checks that each one is documented in as many doc files as you list - catches a command you added to code but forgot to add to the docs, or a rename that only got fixed in one place.

> [!NOTE]
> Alias registrations (`SLASH_COMMANDS["/x"] = SLASH_COMMANDS["/y"]`) are automatically excluded - these are intentional shortcuts, not meant to be individually documented, and including them would produce constant false positives.

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
      - uses: MPHONlC/eso-slash-command-doc-check@Version-0.0.1
        with:
          doc_files: |
            README_BBCODE.txt
            README.md
            README_COMMONMARK.txt
```

`doc_files` accepts any number of files - one per line, or comma-separated on one line.

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `source_glob` | No | `**/*.lua` | Recursive glob matching your Lua source. |
| `doc_files` | Yes | - | List of doc files to check, one per line (or comma-separated). |

## License

MIT - see [LICENSE](LICENSE).
