#!/usr/bin/env python3
"""Append a hot-meme record to references/evolving-hot-memes.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEAT_VALUES = {"A", "B", "C"}
INCLUDE_VALUES = {"是", "否"}
TABLE_HEADER = "| 发现日期 | 梗/热词 | 平台 | 首次看到位置/链接 | 释义 | 典型用法 | 热度判断 | 是否加入总表 |"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_target() -> Path:
    return skill_root() / "references" / "evolving-hot-memes.md"


def clean_cell(value: str) -> str:
    value = value.strip().replace("\r", " ").replace("\n", " ")
    return value.replace("|", "/")


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Target file not found: {path}")
    return path.read_text(encoding="utf-8")


def existing_memes(markdown: str) -> set[str]:
    memes: set[str] = set()
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        if cells[1] in {"梗/热词", "---"}:
            continue
        memes.add(cells[1])
    return memes


def build_row(args: argparse.Namespace) -> str:
    values = [
        args.date,
        args.meme,
        args.platform,
        args.source,
        args.meaning,
        args.usage,
        args.heat,
        args.include,
    ]
    return "| " + " | ".join(clean_cell(value) for value in values) + " |"


def append_row(path: Path, row: str) -> None:
    markdown = load_text(path)
    lines = markdown.splitlines()

    insert_at = None
    for index, line in enumerate(lines):
        if line.startswith("## 热度判断建议"):
            insert_at = index
            break
    if insert_at is None:
        lines.append(row)
    else:
        while insert_at > 0 and lines[insert_at - 1] == "":
            insert_at -= 1
        lines.insert(insert_at, row)
        lines.insert(insert_at + 1, "")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append a hot meme to evolving-hot-memes.md")
    parser.add_argument("--date", required=True, help="Discovery date, YYYY-MM-DD")
    parser.add_argument("--meme", required=True, help="Hot meme or phrase")
    parser.add_argument("--platform", required=True, help="Observed platform, such as 抖音/B站/小红书")
    parser.add_argument("--source", required=True, help="First observed URL or source note")
    parser.add_argument("--meaning", required=True, help="One-sentence meaning")
    parser.add_argument("--usage", required=True, help="Typical usage example")
    parser.add_argument("--heat", required=True, choices=sorted(HEAT_VALUES), help="A/B/C heat confidence")
    parser.add_argument("--include", required=True, choices=sorted(INCLUDE_VALUES), help="是否加入总表: 是/否")
    parser.add_argument("--file", default=str(default_target()), help="Target evolving-hot-memes.md path")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not DATE_RE.match(args.date):
        print("ERROR: --date must use YYYY-MM-DD format", file=sys.stderr)
        return 2

    path = Path(args.file)
    markdown = load_text(path)
    if TABLE_HEADER not in markdown:
        print("ERROR: target file does not contain the expected hot-meme table", file=sys.stderr)
        return 2

    meme = clean_cell(args.meme)
    if meme in existing_memes(markdown):
        print(f"SKIP: meme already exists: {meme}")
        return 0

    append_row(path, build_row(args))
    print(f"ADDED: {meme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
