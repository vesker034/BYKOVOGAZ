# -*- coding: utf-8 -*-
"""Исправление порядка абзацев мобильного блока в п. 2.9 (текст → рис. 35 → рис. 36)."""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document

DOCX_PATH = Path(r"c:\Users\andre\Downloads\Telegram Desktop\filippovdiplom11-1.docx")


def main() -> int:
    if not DOCX_PATH.is_file():
        print("Не найден:", DOCX_PATH, file=sys.stderr)
        return 1

    doc = Document(str(DOCX_PATH))
    paras = doc.paragraphs

    i_start = None
    i_end = None
    for i, p in enumerate(paras):
        t = (p.text or "").strip()
        if t.startswith("Рисунок 34."):
            i_start = i + 1
        if i_start is not None and t.startswith("2.10 Оптимизация"):
            i_end = i
            break
    if i_start is None or i_end is None or i_end <= i_start:
        print("Не найден диапазон мобильного блока", file=sys.stderr)
        return 1

    chunk = [(i, paras[i]) for i in range(i_start, i_end)]

    def pick(pred):
        for i, p in chunk:
            if pred(p):
                return i, p
        raise LookupError(str(pred))

    def picks_empty():
        return [(i, p) for i, p in chunk if not (p.text or "").strip()]

    i_body, _ = pick(lambda p: "Отдельно фиксировалась" in (p.text or ""))
    i_ph1, _ = pick(lambda p: "главная страница в режиме эмуляции мобильного" in (p.text or ""))
    i_ph2, _ = pick(lambda p: "другой раздел сайта" in (p.text or ""))
    i_c35, _ = pick(lambda p: (p.text or "").strip().startswith("Рисунок 35."))
    i_c36, _ = pick(lambda p: (p.text or "").strip().startswith("Рисунок 36."))

    empties = picks_empty()
    if len(empties) != 4:
        print("Ожидалось 4 пустых абзаца в блоке, найдено", len(empties), file=sys.stderr)
        return 1
    empties.sort(key=lambda x: x[0])
    ie1, ie2, ie3, ie4 = [e[0] for e in empties]

    ordered_indices = [i_body, ie1, i_ph1, ie2, i_c35, ie3, i_ph2, ie4, i_c36]

    anchor_after = paras[i_start - 1]._element
    parent = anchor_after.getparent()
    if parent is None:
        return 1

    elements = [paras[i]._element for i in ordered_indices]
    for el in elements:
        p = el.getparent()
        if p is not None:
            p.remove(el)

    cur = anchor_after
    for el in elements:
        cur.addnext(el)
        cur = el

    doc.save(str(DOCX_PATH))
    print("Порядок мобильного блока исправлен:", DOCX_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
