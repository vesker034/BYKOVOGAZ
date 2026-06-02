"""Служебный скрипт: уникальные строки из {% trans %} и {% blocktrans %} в шаблонах."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


def main() -> None:
    msgs: set[str] = set()
    trans_re = re.compile(r"\{%\s*trans\s*(['\"])(?P<s>.*?)\1\s*%\}", re.DOTALL)
    block_re = re.compile(
        r"\{%\s*blocktrans\s+trimmed\s*%\}\s*(?P<body>.*?)\{%\s*endblocktrans\s*%\}",
        re.DOTALL,
    )
    for p in TEMPLATES.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        for m in trans_re.finditer(t):
            msgs.add(m.group("s"))
        for m in block_re.finditer(t):
            body = re.sub(r"\s+", " ", m.group("body")).strip()
            if body:
                msgs.add(body)
    print("unique", len(msgs))
    for s in sorted(msgs, key=lambda x: (len(x), x)):
        print(len(s), s.replace("\n", " ")[:120])


if __name__ == "__main__":
    main()
