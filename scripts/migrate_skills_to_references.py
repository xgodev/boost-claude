#!/usr/bin/env python3
"""One-time migration: flatten skills/boost-*/SKILL.md bodies into skills/boost/references/**/*.md.

Deleted after use in Task 3 — it assumes the pre-migration skills/boost-*/ layout,
which will no longer exist once the migration is complete.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "skills"
DST = REPO / "skills" / "boost" / "references"

SPECIAL = {
    "boost-start": "start.md",
    "boost-model-errors": "model-errors.md",
    "boost-maintainer": "CONTRIBUTING.md",
}

SKIP = {"boost", "gqlgen-field-resolvers"}

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
REF_RE = re.compile(r"`(boost-[a-z0-9-]+)`")


def target_rel_path(skill_name):
    if skill_name in SPECIAL:
        return SPECIAL[skill_name]
    name = skill_name[len("boost-"):]
    group, _, rest = name.partition("-")
    return f"{group}/{rest}.md"


def strip_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    return text[m.end():].lstrip("\n") if m else text


def rewrite_refs(body, name_to_path):
    def repl(match):
        name = match.group(1)
        if name in name_to_path:
            return f"`references/{name_to_path[name]}`"
        return match.group(0)
    return REF_RE.sub(repl, body)


def main():
    skill_dirs = sorted(
        p for p in SRC.iterdir()
        if p.is_dir() and p.name not in SKIP
    )
    name_to_path = {d.name: target_rel_path(d.name) for d in skill_dirs}

    for d in skill_dirs:
        src_file = d / "SKILL.md"
        text = src_file.read_text()
        body = strip_frontmatter(text)
        body = rewrite_refs(body, name_to_path)

        out_path = DST / name_to_path[d.name]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(body)
        print(f"{d.name} -> {out_path.relative_to(REPO)}")

    print(f"\nMigrated {len(skill_dirs)} skills.")


if __name__ == "__main__":
    main()
