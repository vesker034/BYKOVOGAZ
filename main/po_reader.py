"""Разбор простых блоков msgid/msgstr из django.po (без зависимостей)."""

from __future__ import annotations

import codecs
import re
from pathlib import Path


def _decode_po_fragment(fragment: str) -> str:
    return codecs.decode(fragment, "unicode_escape").replace("\r\n", "\n").replace("\r", "\n")


def _literal_strings_on_line(rest: str) -> list[str]:
    items: list[str] = []
    for m in re.finditer(r'"(?:[^"\\]|\\.)*"', rest):
        raw_inner = m.group(0)[1:-1]
        items.append(_decode_po_fragment(raw_inner))
    return items


def _read_bundle(lines: list[str], start: int, prefix: str) -> tuple[int, str]:
    line = lines[start].strip()
    if not line.startswith(prefix):
        raise ValueError(f"Ожидалась строка с {prefix}: {lines[start]!r}")
    remainder = line[len(prefix) :].strip()
    parts: list[str] = []
    parts.extend(_literal_strings_on_line(remainder))
    idx = start + 1
    while idx < len(lines):
        cand = lines[idx].strip()
        if not cand.startswith('"'):
            break
        parts.extend(_literal_strings_on_line(cand))
        idx += 1
    return idx, "".join(parts)


def iter_po_pairs(path: Path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("msgid "):
            i += 1
            continue

        i, mid = _read_bundle(lines, i, "msgid ")
        while i < len(lines) and not lines[i].strip().startswith("msgstr"):
            if lines[i].strip().startswith("#") or lines[i].strip() == "":
                i += 1
                continue
            i += 1
        if i >= len(lines) or not lines[i].strip().startswith("msgstr"):
            raise ValueError("Не найден msgstr после msgid")
        i, mstr = _read_bundle(lines, i, "msgstr ")
        if mid == "":
            continue
        yield mid, mstr
