# -*- coding: utf-8 -*-
"""Подгонка ax.set_ylim по фактической рамке содержимого (без искусственных полей по Y)."""

from __future__ import annotations

import matplotlib.pyplot as plt


def apply_vertical_fit_from_artists(
    ax,
    fig: plt.Figure,
    *,
    pad_px: float = 0.0,
) -> tuple[float, float]:
    """
    По видимым artist'ам аккумулирует bbox в пикселях, переводит в координаты данных,
    выставляет ylim без лишней полосы сверху/снизу.
    Строки сетки (zorder<=0 по умолчанию у mpl) пропускаются.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ymin = float("inf")
    ymax = float("-inf")
    rng_x = ax.get_xlim()[1] - ax.get_xlim()[0]
    rng_y = ax.get_ylim()[1] - ax.get_ylim()[0]
    if rng_y <= 0:
        rng_y = 1.0

    inv = ax.transData.inverted()

    def acc_disp_xy(x_px: float, y_px: float) -> None:
        nonlocal ymin, ymax
        xd, yd = inv.transform((x_px, y_px))
        ymin = min(ymin, yd)
        ymax = max(ymax, yd)

    for line in ax.lines:
        if line.get_visible() is False:
            continue
        if float(line.get_zorder()) <= 0.0:
            continue
        xd = abs(float(line.get_xdata()[1]) - float(line.get_xdata()[0]))
        yd = abs(float(line.get_ydata()[1]) - float(line.get_ydata()[0]))
        # отбраковка типичной сеточной оси-тянучки через всё окно данных
        if xd < 1e-9 * max(rng_x, 1.0) and yd >= 0.85 * rng_y:
            continue
        if yd < 1e-9 * max(rng_y, 1.0) and xd >= 0.85 * rng_x:
            continue
        try:
            bb = line.get_window_extent(renderer)
        except (AttributeError, RuntimeError):
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        for x_px, y_px in bb.corners():
            acc_disp_xy(x_px, y_px)

    tbl = getattr(ax, "tables", {}) or {}
    tbl_vals = list(tbl.values()) if isinstance(tbl, dict) else []

    for p in [*ax.patches, *tbl_vals]:
        if p.get_visible() is False:
            continue
        try:
            bb = p.get_window_extent(renderer)
        except (AttributeError, RuntimeError):
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        for x_px, y_px in bb.corners():
            acc_disp_xy(x_px, y_px)

    for t in ax.texts:
        if t.get_visible() is False:
            continue
        try:
            bb = t.get_window_extent(renderer)
        except (AttributeError, RuntimeError):
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        for x_px, y_px in bb.corners():
            acc_disp_xy(x_px, y_px)

    for c in ax.collections:
        if c.get_visible() is False:
            continue
        try:
            bb = c.get_window_extent(renderer)
        except (AttributeError, RuntimeError):
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        for x_px, y_px in bb.corners():
            acc_disp_xy(x_px, y_px)

    for a in ax.artists:
        if a.get_visible() is False:
            continue
        if not hasattr(a, "get_window_extent"):
            continue
        try:
            bb = a.get_window_extent(renderer)
        except (AttributeError, RuntimeError):
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        for x_px, y_px in bb.corners():
            acc_disp_xy(x_px, y_px)

    if not ymin < ymax:
        raise RuntimeError("apply_vertical_fit_from_artists: не удалось оценить границы по Y")

    h_px = ax.bbox.height
    dy = (ymax - ymin) * (pad_px / h_px) if h_px > 0 else 0.0
    ax.set_ylim(ymin - dy, ymax + dy)
    return ymin - dy, ymax + dy


__all__ = ["apply_vertical_fit_from_artists"]
