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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-glob', default='**/*.lua')
    parser.add_argument('--esoui-file', default='README_ESOUI.txt')
    parser.add_argument('--github-file', default='README.md')
    parser.add_argument('--bethesda-file', default='README_BETHESDA.txt')
    args = parser.parse_args()

    commands = find_primary_commands(args.source_glob)
    out = ["## Slash command documentation check", ""]

    if not commands:
        out.append(f"No primary SLASH_COMMANDS registrations found under `{args.source_glob}` - nothing to check.")
        print('\n'.join(out))
        return

    out.append(f"Found {len(commands)} primary slash command(s) registered in code: {', '.join(sorted(commands))}")
    out.append("")

    files = [
        ("ESOUI", args.esoui_file),
        ("GitHub", args.github_file),
        ("Bethesda", args.bethesda_file),
    ]

    any_missing = False
    for label, path in files:
        text = read(path)
        if text is None:
            out.append(f"**{label}** (`{path}`): file not found - skipping.")
            continue
        missing = sorted(c for c in commands if c not in text)
        if missing:
            any_missing = True
            out.append(f"**{label}** (`{path}`): missing {len(missing)} command(s): {', '.join(missing)}")
            for c in missing:
                print(f"::error::{label} ({path}) does not document slash command {c}")
        else:
            out.append(f"**{label}** (`{path}`): all commands documented.")

    print('\n'.join(out))
    if any_missing:
        sys.exit(1)


if __name__ == '__main__':
    main()
