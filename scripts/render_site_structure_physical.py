# -*- coding: utf-8 -*-
"""Физическая структура: узлы на сетке; границы осей по содержимому, крупные подписи."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpl_vertical_fit import apply_vertical_fit_from_artists

ROOT_TITLE = "Сайт ООО «Быковогаз» (Django)"
SUBTITLE = "физическая структура каталогов и файлов проекта"

Rows = list[str]
Branch = tuple[str, list[str] | list[list[str]], list[str] | None]

BRANCHES: list[Branch] = [
    ("config/", ["settings.py", "urls.py", "wsgi.py", "asgi.py"], None),
    (
        "main/",
        ["models.py", "views.py", "urls.py", "admin.py", "apps.py", "tests.py"],
        ["migrations/"],
    ),
    ("templates/", ["base.html", "components/", "pages/"], None),
    ("static/", ["css/", "js/", "img/", "tours/"], None),
    ("locale/", ["en/LC_MESSAGES/", "django.po", "django.mo"], None),
    (
        "корень",
        [
            ["manage.py", "requirements.txt", ".env.example"],
            [".gitignore", "README.md"],
        ],
        None,
    ),
]

CH_GAP = 0.12
CHILD_H_FIXED = 0.44
GAP_AFTER_BUS = 0.14
ROW_GAP = 0.32
STEM_DOWN = 0.14
PARENT_W = 1.05
PARENT_H = 0.44
EXTRA_FOLDER_H = 0.38

FOLDER_TAB_FACE = "#c8c8c8"
FOLDER_BODY_FACE = "#f5f3ee"
FILE_FACE = "#ffffff"
OUTLINE_FOLDER_LW = 1.38
OUTLINE_FILE_LW = 0.95


def band_for(h: float) -> float:
    return max(0.11, min(0.16, h * 0.22))


def is_directory_label(label: str) -> bool:
    return label.endswith("/") or label == "корень"


def as_rows(children: list[str] | list[list[str]]) -> list[Rows]:
    if not children:
        return []
    if isinstance(children[0], list):
        return children  # type: ignore[return-value]
    return [children]  # type: ignore[list-item]


def node_width(label: str) -> float:
    if label == "en/LC_MESSAGES/":
        return 2.12
    n = len(label)
    if n > 20:
        return 1.28
    if n > 14:
        return 1.12
    if n > 8:
        return 0.98
    return 0.82


def row_total_width(labels: Rows, gap: float) -> float:
    if not labels:
        return 0.0
    ws = [max(node_width(t), 0.78) for t in labels]
    return sum(ws) + (len(labels) - 1) * gap


def split_row_to_fit(labels: Rows, max_w: float, gap: float) -> list[Rows]:
    if row_total_width(labels, gap) <= max_w or len(labels) <= 1:
        return [labels]
    out: list[Rows] = []
    cur: Rows = []
    cur_w = 0.0
    for lab in labels:
        w = max(node_width(lab), 0.78)
        need = w if not cur else gap + w
        if cur and cur_w + need > max_w:
            out.append(cur)
            cur = [lab]
            cur_w = w
        else:
            cur.append(lab)
            cur_w += need
    if cur:
        out.append(cur)
    return out if len(out) > 1 else [labels]


def normalize_rows_for_lane(rows: list[Rows], lane_width: float, gap: float) -> list[Rows]:
    max_w = max(1.35, lane_width * 0.9)
    merged: list[Rows] = []
    for r in rows:
        if row_total_width(r, gap) <= max_w:
            merged.append(r)
            continue
        merged.extend(split_row_to_fit(r, max_w, gap))
    return merged


def draw_folder(ax, cx: float, y_top: float, w: float, h: float, name: str, fs: float = 10.0) -> float:
    """Папка: полоса вкладки + тело, контрастный фон и жирная обводка (как в учебных схемах)."""
    b = band_for(h)
    x0 = cx - w / 2
    y0 = y_top - h
    ax.add_patch(
        Rectangle(
            (x0, y0),
            w,
            h,
            facecolor=FOLDER_BODY_FACE,
            edgecolor="black",
            linewidth=OUTLINE_FOLDER_LW,
            zorder=4,
        )
    )
    ax.add_patch(
        Rectangle(
            (x0, y_top - b),
            w,
            b,
            facecolor=FOLDER_TAB_FACE,
            edgecolor="black",
            linewidth=1.05,
            zorder=5,
        )
    )
    ax.plot([x0, x0 + w], [y_top - b, y_top - b], color="black", linewidth=1.05, zorder=6)
    ax.text(cx, y_top - b / 2, name, ha="center", va="center", fontsize=fs, fontweight="bold", zorder=7)
    return y0


def draw_child_box(ax, cx: float, y_top: float, w: float, h: float, label: str) -> float:
    """Файл — один прямоугольник; папка — как draw_folder, уменьшенный шрифт."""
    x0 = cx - w / 2
    y0 = y_top - h
    if is_directory_label(label):
        b = band_for(h)
        if len(label) >= 15:
            b = max(b, 0.155)
        ax.add_patch(
            Rectangle(
                (x0, y0),
                w,
                h,
                facecolor=FOLDER_BODY_FACE,
                edgecolor="black",
                linewidth=OUTLINE_FOLDER_LW,
                zorder=4,
            )
        )
        ax.add_patch(
            Rectangle(
                (x0, y_top - b),
                w,
                b,
                facecolor=FOLDER_TAB_FACE,
                edgecolor="black",
                linewidth=1.0,
                zorder=5,
            )
        )
        ax.plot([x0, x0 + w], [y_top - b, y_top - b], color="black", linewidth=1.0, zorder=6)
        ax.text(cx, y_top - b / 2, label, ha="center", va="center", fontsize=8.6, fontweight="bold", zorder=7)
        return y0

    ax.add_patch(
        Rectangle(
            (x0, y0),
            w,
            h,
            facecolor=FILE_FACE,
            edgecolor="black",
            linewidth=OUTLINE_FILE_LW,
            zorder=4,
        )
    )
    fs = 8.4 if len(label) < 15 else 7.8
    ax.text(cx, (y_top + y0) / 2, label, ha="center", va="center", fontsize=fs, zorder=6, clip_on=True)
    return y0


def draw_child_row(
    ax,
    cx: float,
    y_bus: float,
    y_box_top: float,
    labels: Rows,
    h_child: float,
) -> float:
    if not labels:
        return y_bus
    widths: list[float] = []
    for t in labels:
        nw = max(node_width(t), 0.78)
        if not is_directory_label(t):
            nw = max(nw, h_child * 0.9)
        widths.append(nw)
    total = sum(widths) + (len(labels) - 1) * CH_GAP
    x_start = cx - total / 2
    centers: list[float] = []
    acc = x_start
    for w in widths:
        centers.append(acc + w / 2)
        acc += w + CH_GAP

    ax.plot([centers[0], centers[-1]], [y_bus, y_bus], color="#1a1a1a", linewidth=1.15, zorder=3)
    bottoms: list[float] = []
    for lab, cc, w in zip(labels, centers, widths, strict=True):
        ax.add_patch(
            FancyArrowPatch(
                (cc, y_bus),
                (cc, y_box_top + 0.03),
                arrowstyle="-|>",
                mutation_scale=11,
                linewidth=1.05,
                color="#1a1a1a",
                zorder=3,
                shrinkA=0,
                shrinkB=0,
            )
        )
        b = draw_child_box(ax, cc, y_box_top, w, h_child, lab)
        bottoms.append(b)
    return min(bottoms)


def draw_stem_vertical(ax, cx: float, y_hi: float, y_lo: float) -> None:
    ax.plot([cx, cx], [y_hi, y_lo], color="#1a1a1a", linewidth=1.1, zorder=3)


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "docs" / "site-structure-physical.png"
    fig, ax = plt.subplots(figsize=(17.0, 11.0), dpi=200)
    fig.patch.set_facecolor("#eeeeee")
    ax.set_facecolor("#eeeeee")

    x_margin_lo = 0.35
    x_margin_hi = 0.35
    W = 16.0
    X0 = x_margin_lo
    X1 = W - x_margin_hi
    x_usable = X1 - X0

    n_cols = len(BRANCHES)
    lane_w = x_usable / n_cols
    col_centers = [X0 + lane_w * (i + 0.5) for i in range(n_cols)]
    cx_root = X0 + x_usable / 2

    y_layout_top = 10.35
    ax.axis("off")

    yt = y_layout_top - 0.06
    ax.text(cx_root, yt, ROOT_TITLE, ha="center", fontsize=15.5, fontweight="bold", zorder=6)
    yt -= 0.38
    ax.text(cx_root, yt, SUBTITLE, ha="center", fontsize=11.0, color="#222222", zorder=6)
    yt -= 0.42

    root_w = min(7.2, x_usable * 0.52)
    root_h = 0.52
    root_top = yt
    root_bottom = draw_folder(ax, cx_root, root_top, root_w, root_h, "проект веб-сайта", fs=11.5)
    yt = root_bottom - 0.38

    y_joint = yt
    x_bus_left = col_centers[0] - PARENT_W / 2
    x_bus_right = col_centers[-1] + PARENT_W / 2
    ax.plot([cx_root, cx_root], [root_bottom, y_joint], color="#1a1a1a", linewidth=1.2, zorder=2)
    ax.plot([x_bus_left, x_bus_right], [y_joint, y_joint], color="#1a1a1a", linewidth=1.2, zorder=2)

    yt -= 0.26
    y_parent_top = yt
    p_bottom = y_parent_top - PARENT_H

    y_bus_global = p_bottom - STEM_DOWN
    y_child_top_global = y_bus_global - GAP_AFTER_BUS

    row_lists_raw = [as_rows(ch) for _, ch, _ in BRANCHES]
    row_lists = [normalize_rows_for_lane(rl, lane_w, CH_GAP) for rl in row_lists_raw]

    content_y_min = root_bottom

    for (parent, _children, extra), cx, rows in zip(BRANCHES, col_centers, row_lists, strict=True):
        ax.add_patch(
            FancyArrowPatch(
                (cx, y_joint),
                (cx, y_parent_top),
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=1.1,
                color="#1a1a1a",
                zorder=3,
                shrinkB=1,
            )
        )
        pb = draw_folder(ax, cx, y_parent_top, PARENT_W, PARENT_H, parent, fs=9.8)
        draw_stem_vertical(ax, cx, pb, y_bus_global)

        y_row_top = y_child_top_global
        y_min_col: float | None = None
        y_bus_row = y_bus_global
        for r_i, row_labels in enumerate(rows):
            if r_i > 0 and y_min_col is not None:
                y_bus_row = y_min_col - ROW_GAP
                draw_stem_vertical(ax, cx, y_min_col - 0.03, y_bus_row)
                y_row_top = y_bus_row - GAP_AFTER_BUS
            y_min_col = draw_child_row(ax, cx, y_bus_row, y_row_top, row_labels, CHILD_H_FIXED)

        lowest = y_min_col if y_min_col is not None else y_bus_global
        if extra and y_min_col is not None:
            y_stem0 = y_min_col - 0.16
            ax.plot([cx, cx], [y_min_col, y_stem0], color="#1a1a1a", linewidth=1.05, zorder=3)
            y_cursor = y_stem0 - 0.06
            for name in extra:
                w = max(node_width(name) + 0.12, 0.95)
                y0 = draw_folder(ax, cx, y_cursor, w, EXTRA_FOLDER_H, name, fs=9.0)
                lowest = min(lowest, y0)
                y_cursor = y0 - 0.12

        content_y_min = min(content_y_min, lowest)

    pad_x = 0.14
    x_lim_lo = X0 - pad_x
    x_lim_hi = X1 + pad_x
    y_prov_hi = y_layout_top + 2.8
    y_prov_lo = content_y_min - 2.8

    ax.set_xlim(x_lim_lo, x_lim_hi)
    ax.set_ylim(y_prov_lo, y_prov_hi)
    ax.set_aspect("auto")

    apply_vertical_fit_from_artists(ax, fig, pad_px=0.0)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(out, bbox_inches="tight", pad_inches=0.0, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
