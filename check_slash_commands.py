import re
import sys
import glob
import argparse

PRIMARY_RE = re.compile(r'SLASH_COMMANDS\s*\[\s*"(/[A-Za-z0-9_]+)"\s*\]\s*=\s*function')
ALIAS_RE = re.compile(r'SLASH_COMMANDS\s*\[\s*"(/[A-Za-z0-9_]+)"\s*\]\s*=\s*SLASH_COMMANDS\s*\[')


def read(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


def find_primary_commands(source_glob):
    primary = set()
    aliased = set()
    for path in sorted(glob.glob(source_glob, recursive=True)):
        text = read(path)
        if text is None:
            continue
        for m in PRIMARY_RE.finditer(text):
            primary.add(m.group(1))
        for m in ALIAS_RE.finditer(text):
            aliased.add(m.group(1))
    return primary - aliased


def parse_doc_files(raw):
    files = []
    for chunk in raw.replace(',', '\n').splitlines():
        chunk = chunk.strip()
        if chunk:
            files.append(chunk)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-glob', default='**/*.lua')
    parser.add_argument('--doc-files', required=True)
    args = parser.parse_args()

    commands = find_primary_commands(args.source_glob)
    doc_files = parse_doc_files(args.doc_files)
    out = ["## Slash command documentation check", ""]

    if not commands:
        out.append(f"No primary SLASH_COMMANDS registrations found under `{args.source_glob}` - nothing to check.")
        print('\n'.join(out))
        return

    out.append(f"Found {len(commands)} primary slash command(s) registered in code: {', '.join(sorted(commands))}")
    out.append("")

    any_missing = False
    for path in doc_files:
        text = read(path)
        if text is None:
            out.append(f"**`{path}`**: file not found - skipping.")
            continue
        missing = sorted(c for c in commands if c not in text)
        if missing:
            any_missing = True
            out.append(f"**`{path}`**: missing {len(missing)} command(s): {', '.join(missing)}")
            for c in missing:
                print(f"::error::{path} does not document slash command {c}")
        else:
            out.append(f"**`{path}`**: all commands documented.")

    print('\n'.join(out))
    if any_missing:
        sys.exit(1)


if __name__ == '__main__':
    main()
