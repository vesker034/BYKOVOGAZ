# -*- coding: utf-8 -*-
"""ER-схема в стиле «таблицы на сетке»: PK/FK в узкой колонке, стрелки 1:N.

Раскладка считается автоматически по колонкам (без наложений).
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpl_vertical_fit import apply_vertical_fit_from_artists

TABLES: dict[str, list[tuple[str, str]]] = {
    "candidate_statuses": [
        ("PK", "status_id"),
        ("", "name"),
    ],
    "candidate_profiles": [
        ("PK", "candidate_id"),
        ("", "full_name"),
        ("", "phone, email"),
        ("", "desired_position"),
        ("", "message"),
        ("FK", "status_id"),
        ("", "created_at"),
    ],
    "candidate_attachments": [
        ("PK", "attachment_id"),
        ("FK", "candidate_id"),
        ("", "file_path"),
        ("", "uploaded_at"),
    ],
    "departments": [
        ("PK", "department_id"),
        ("", "name"),
    ],
    "team_members": [
        ("PK", "member_id"),
        ("", "first_name, last_name"),
        ("", "position"),
        ("", "photo"),
        ("", "bio"),
        ("FK", "department_id (опц.)"),
        ("", "created_at"),
    ],
    "social_links": [
        ("PK", "social_id"),
        ("", "name"),
        ("", "base_url (опц.)"),
    ],
    "member_social_links": [
        ("FK", "member_id"),
        ("FK", "social_id"),
        ("", "url_or_value"),
        ("PK", "(member_id, social_id)"),
    ],
    "roles": [
        ("PK", "role_id"),
        ("", "name"),
    ],
    "users": [
        ("PK", "user_id"),
        ("", "login"),
        ("", "password_hash"),
        ("", "email"),
        ("", "created_at"),
        ("", "updated_at"),
    ],
    "user_roles": [
        ("FK", "user_id"),
        ("FK", "role_id"),
        ("PK", "(user_id, role_id)"),
    ],
    "contact_messages": [
        ("PK", "message_id"),
        ("", "name"),
        ("", "phone или email"),
        ("", "subject (опц.)"),
        ("", "message"),
        ("", "created_at"),
        ("FK", "processed_by_user_id (опц.)"),
    ],
    "contact_message_attachments": [
        ("PK", "attachment_id"),
        ("FK", "message_id"),
        ("", "file_path"),
        ("", "uploaded_at"),
    ],
}

EDGES: list[tuple[str, str, bool]] = [
    ("candidate_statuses", "candidate_profiles", False),
    ("candidate_profiles", "candidate_attachments", False),
    ("departments", "team_members", False),
    ("team_members", "member_social_links", False),
    ("social_links", "member_social_links", False),
    ("users", "user_roles", True),
    ("roles", "user_roles", True),
    ("contact_messages", "contact_message_attachments", False),
    ("users", "contact_messages", False),
]

W_TABLE = 3.18
LINE_H = 0.46
TITLE_H = 0.54
KEY_W = 0.56
TITLE_FS = 11.8
KEY_FS = 9.0
FIELD_FS = 10.2

TABLE_EDGE_LW = 2.05
GRID_LINE_LW = 0.95
PK_LINE_LW = 0.85

# вертикальный зазор между нижним краем одной таблицы и верхнем следующей
ROW_GAP = 0.62
Y_TOP = 10.35


def table_height(rows: int) -> float:
    return TITLE_H + rows * LINE_H


def vertical_extent(pos: dict[str, tuple[float, float]]) -> tuple[float, float]:
    """Нижняя и верхняя координаты по всем таблицам (грань рамок)."""
    y_lo = float("inf")
    y_hi = float("-inf")
    for name, (x0, y0) in pos.items():
        h = table_height(len(TABLES[name]))
        y_lo = min(y_lo, y0)
        y_hi = max(y_hi, y0 + h)
    return y_lo, y_hi


def build_positions() -> dict[str, tuple[float, float]]:
    """Колонки сверху вниз; соседние колонки разнесены по X, пересечений по Y нет."""

    def stack(names: list[str], x: float, y_top: float) -> dict[str, tuple[float, float]]:
        out: dict[str, tuple[float, float]] = {}
        y = y_top
        for nm in names:
            h = table_height(len(TABLES[nm]))
            y -= h
            out[nm] = (x, y)
            y -= ROW_GAP
        return out

    gap = 0.52
    x1 = 0.28
    x2 = x1 + W_TABLE + gap
    x_ca = x2 + W_TABLE + gap * 0.65
    x_users = x_ca + W_TABLE + gap * 0.85
    x_contact = x_users + W_TABLE + gap * 0.85

    pos: dict[str, tuple[float, float]] = {}
    pos.update(
        stack(
            ["candidate_statuses", "departments", "social_links", "roles"],
            x1,
            Y_TOP,
        )
    )
    pos.update(stack(["candidate_profiles", "team_members", "member_social_links"], x2, Y_TOP))
    h_ca = table_height(len(TABLES["candidate_attachments"]))
    pos["candidate_attachments"] = (x_ca, Y_TOP - h_ca)

    pos.update(stack(["users", "user_roles"], x_users, Y_TOP))

    pos.update(stack(["contact_messages", "contact_message_attachments"], x_contact, Y_TOP))
    return pos


def draw_table(ax, name: str, rows: list[tuple[str, str]], pos: tuple[float, float]) -> dict:
    x0, y0 = pos
    h = table_height(len(rows))
    ax.add_patch(
        Rectangle(
            (x0, y0),
            W_TABLE,
            h,
            facecolor="white",
            edgecolor="black",
            linewidth=TABLE_EDGE_LW,
            zorder=3,
        )
    )
    ax.plot(
        [x0, x0 + W_TABLE],
        [y0 + h - TITLE_H, y0 + h - TITLE_H],
        color="black",
        linewidth=1.25,
        zorder=4,
    )
    ax.text(
        x0 + W_TABLE / 2,
        y0 + h - TITLE_H / 2,
        name,
        ha="center",
        va="center",
        fontsize=TITLE_FS,
        fontweight="bold",
        zorder=4,
        clip_on=True,
    )
    y = y0 + h - TITLE_H
    key_sep_x = x0 + KEY_W
    for kt, fname in rows:
        y -= LINE_H
        ax.plot([x0, x0 + W_TABLE], [y, y], color="#b8b8b8", linewidth=GRID_LINE_LW, zorder=3)
        ax.plot([key_sep_x, key_sep_x], [y, y + LINE_H], color="black", linewidth=PK_LINE_LW, zorder=3)
        if kt:
            ax.text(
                x0 + KEY_W / 2,
                y + LINE_H / 2,
                kt,
                ha="center",
                va="center",
                fontsize=KEY_FS,
                zorder=4,
                clip_on=True,
            )
        ax.text(
            key_sep_x + 0.06,
            y + LINE_H / 2,
            fname,
            ha="left",
            va="center",
            fontsize=FIELD_FS,
            zorder=4,
            clip_on=True,
        )

    mid_y = y0 + (h - TITLE_H) / 2
    return {
        "x0": x0,
        "y0": y0,
        "w": W_TABLE,
        "h": h,
        "title_h": TITLE_H,
        "mid_y": mid_y,
        "right": x0 + W_TABLE,
        "left": x0,
        "top": y0 + h,
    }


def main() -> int:
    out_png = Path(__file__).resolve().parents[1] / "docs" / "plan-db-schema.png"
    out_svg = Path(__file__).resolve().parents[1] / "docs" / "plan-db-schema.svg"

    pos = build_positions()
    x_right = max(x0 + W_TABLE for x0, _ in pos.values())
    xmin_tables = min(x0 for x0, _ in pos.values())
    xmax = x_right + 0.32
    y_bottom, y_top = vertical_extent(pos)
    title_y_baseline = y_top + 0.06
    # Временный ylim на отрисовку; после контента задаётся фактический bbox по объектам (без полей сверху/снизу).
    ylim_prov_lo = y_bottom - 2.8
    ylim_prov_hi = title_y_baseline + 2.8

    fig_w, fig_h = 21.5, 10.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.patch.set_facecolor("#f0f0f0")
    ax.set_facecolor("#f0f0f0")

    ax.set_xlim(xmin_tables - 0.1, xmax)
    ax.set_ylim(ylim_prov_lo, ylim_prov_hi)
    ax.axis("off")
    # Без equal: иначе на широком окне «сплющивается» вертикаль и таблицы визуально наезжают.

    ax.grid(True, color="#d6d6d6", linewidth=0.55, alpha=0.95, zorder=0)
    ax.set_xticks([i * 0.5 for i in range(int(2 * xmin_tables) - 2, int(2 * xmax) + 6)])
    ax.set_yticks([i * 0.5 for i in range(int(2 * ylim_prov_lo) - 2, int(2 * ylim_prov_hi) + 6)])
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    ax.text(
        xmax / 2,
        title_y_baseline,
        "Логическая схема базы данных веб-сайта",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        clip_on=False,
    )

    bboxes: dict[str, dict] = {}
    for tname, rows in TABLES.items():
        bboxes[tname] = draw_table(ax, tname, rows, pos[tname])

    for a, b, dashed in EDGES:
        ba, bb = bboxes[a], bboxes[b]
        horiz_gap = bb["left"] - ba["right"]
        if horiz_gap > 0.15:
            x1, y1 = ba["right"], ba["mid_y"]
            x2, y2 = bb["left"], bb["mid_y"]
        else:
            x1, y1 = ba["x0"] + ba["w"] / 2, ba["y0"]
            x2, y2 = bb["x0"] + bb["w"] / 2, bb["top"]
        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.35,
            color="#0d0d0d",
            linestyle="--" if dashed else "-",
            zorder=2,
            shrinkA=2,
            shrinkB=2,
        )
        ax.add_patch(arrow)
        if not dashed:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my + 0.16,
                "1:N",
                ha="center",
                va="bottom",
                fontsize=9.0,
                fontweight="bold",
                color="#111111",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.16", facecolor="#f5f5f5", edgecolor="#666666", linewidth=1.05, alpha=0.94),
            )

    apply_vertical_fit_from_artists(ax, fig, pad_px=0.0)
    y_lim_lo_f, y_lim_hi_f = ax.get_ylim()
    ax.set_yticks([i * 0.5 for i in range(int(2 * y_lim_lo_f) - 1, int(2 * y_lim_hi_f) + 4)])
    ax.set_xticks([i * 0.5 for i in range(int(2 * xmin_tables) - 2, int(2 * xmax) + 6)])

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(out_png, bbox_inches="tight", pad_inches=0.0, facecolor=fig.get_facecolor(), edgecolor="none")
    fig.savefig(out_svg, bbox_inches="tight", pad_inches=0.0, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("PNG:", out_png)
    print("SVG:", out_svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
