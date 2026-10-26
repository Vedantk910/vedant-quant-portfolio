"""Generate the six output charts, light + dark variants, from real project data."""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Finance Projects")
OUT = ROOT / "portfolio-site" / "img"
OUT.mkdir(exist_ok=True)

# Two palettes so each chart reads on its own card surface in both themes.
LIGHT = dict(canvas="#ffffff", ink="#1d1d1f", muted="#86868b",
             accent="#a3132e", accent2="#c98b93", grid=(0.0,0.0,0.0,0.08))
DARK  = dict(canvas="#1d1d1f", ink="#f5f5f7", muted="#a1a1a6",
             accent="#e8929b", accent2="#96505b", grid=(1.0,1.0,1.0,0.14))

C = {}     # active palette (mutated in place per theme batch)
SFX = ""   # active filename suffix ("", or "-dark")

def apply_rc(P):
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial"],
        "figure.facecolor": P["canvas"], "axes.facecolor": P["canvas"],
        "axes.edgecolor": P["grid"], "axes.linewidth": 1,
        "text.color": P["ink"], "xtick.color": P["muted"], "ytick.color": P["muted"],
        "axes.labelcolor": P["muted"], "axes.titlecolor": P["ink"],
    })

def style(ax, xgrid=False):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(C["grid"]); ax.spines["bottom"].set_color(C["grid"])
    ax.set_facecolor(C["canvas"])
    ax.grid(axis="y" if not xgrid else "x", color=C["grid"], lw=0.8, alpha=0.85)
    ax.set_axisbelow(True)

def save(name, fig):
    # Force theme-aware facecolor + tick colors on every axis (incl. colorbar).
    # Without this the dark batch falls back to matplotlib defaults (white axes,
    # black ticks) and the notations disappear against the dark card surface.
    for ax in fig.axes:
        ax.set_facecolor(C["canvas"])
        for t in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
            t.set_color(C["muted"])
    fig.tight_layout()
    base = Path(name).stem
    fig.savefig(OUT / (base + SFX + ".png"), facecolor=C["canvas"], bbox_inches="tight")
    plt.close(fig)

def chart_p1():
    d = pd.read_csv(ROOT / "quant-ml-factor-backtest" / "out" / "compare_models.csv")
    d = d.sort_values("sharpe", ascending=False)
    labels = [f"{m} - {'sector-neutral' if sn else 'plain'}"
              for m, sn in zip(d["model"], d["sector_neutral"])]
    fig, ax = plt.subplots(figsize=(6, 3.4), dpi=200)
    rev_vals = list(d["sharpe"].values[::-1]); rev_lab = labels[::-1]
    cols = [C["accent"] if v >= 1.2 else C["muted"] for v in rev_vals]
    bars = ax.barh(rev_lab, rev_vals, height=0.6, color=cols)
    for r, v in zip(bars, rev_vals):
        ax.text(v + 0.03, r.get_y() + r.get_height()/2, f"{v:.2f}", va="center", fontsize=9, color=C["ink"])
    ax.axvline(1.0, color=C["muted"], lw=1, ls="--", alpha=0.6)
    ax.text(1.02, len(rev_vals)-0.35, "equal-weight hurdle", fontsize=8, color=C["muted"], va="top")
    ax.set_xlim(0, 1.7); style(ax)
    ax.set_title("Out-of-sample Sharpe by model and allocation, walk-forward 2023 / 2024",
                 fontsize=10, pad=12, loc="left")
    ax.set_yticklabels(rev_lab, fontsize=8)
    save("p1_sharpe.png", fig)

def chart_p2():
    import json
    d = json.loads((ROOT / "garch-var-desk" / "out" / "desk_numbers.json").read_text())
    vt, bm = d["vol_target_metrics"], d["benchmark_metrics"]
    rows = [("15% vol-target", vt["sharpe"], C["accent"]), ("50/50 static", bm["sharpe"], C["muted"])]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 2.8), dpi=200)
    for ax, key, ttl in ((ax1, "sharpe", "Annualised Sharpe"), (ax2, "max_drawdown", "Max drawdown")):
        vals = [r[1] for r in rows]
        b = ax.bar([r[0] for r in rows], vals, width=0.5, color=[r[2] for r in rows])
        ax.set_ylim(0, max(vals) * 1.3)
        for r, v in zip(b, vals):
            ax.text(r.get_x() + r.get_width()/2, v + max(vals)*0.02, f"{v:.2f}",
                    ha="center", fontsize=11, color=C["ink"])
        ax.set_title(ttl, fontsize=9, pad=8, loc="left"); style(ax); ax.set_yticklabels([])
    ax1.set_title(f"Annualised Sharpe  \u00b7  GARCH-t persistence {d['garch_t']['persistence']:.3f}",
                 fontsize=9, pad=8, loc="left")
    save("p2_vartarget.png", fig)

def chart_p3():
    sys.path.insert(0, str(ROOT / "ma-case-file"))
    from model.accretive import accretion_grid
    g = accretion_grid()
    fig, ax = plt.subplots(figsize=(6, 2.6), dpi=200)
    im = ax.imshow(g.values * 100, cmap="RdYlGn_r", aspect="auto", vmin=-2, vmax=4)
    ax.set_xticks(range(len(g.columns)), list(g.columns), fontsize=8)
    ax.set_yticks(range(len(g.index)), [i.replace(" capture", "") for i in g.index], fontsize=8)
    for i in range(len(g.index)):
        for j in range(len(g.columns)):
            v = g.values[i, j] * 100
            # cell text: white on the dark map cells, fixed dark ink on the light
            # ones - the colormap is theme-independent, so this rule holds in both
            ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=8.5,
                    color="white" if abs(v) > 1.5 else "#1d1d1f")
    ax.set_title("Year-1 EPS accretion % by entry multiple and synergy capture", fontsize=10, pad=10, loc="left")
    for s in ax.spines.values(): s.set_visible(False)
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.08); cb.set_label("%", fontsize=8, color=C["muted"])
    cb.ax.tick_params(labelsize=8, colors=C["muted"])
    save("p3_accretion.png", fig)

def chart_p4():
    d = pd.read_csv(ROOT / "patchtst-forecast" / "out" / "ablation.csv")
    fig, ax = plt.subplots(figsize=(6, 2.9), dpi=200)
    models = ["random_walk", "ets", "lightgbm", "patchtst"]
    h5 = d[d["horizon"] == 5].set_index("model")["mae"]; h10 = d[d["horizon"] == 10].set_index("model")["mae"]
    xs = np.arange(len(models)); w = 0.36
    ax.bar(xs - w/2, [h5[m] for m in models], w, label="horizon 5", color=C["muted"])
    ax.bar(xs + w/2, [h10[m] for m in models], w, label="horizon 10", color=C["accent"])
    ax.set_xticks(xs, models, fontsize=8)
    ax.set_ylabel("MAE (DXY monthly returns)", fontsize=9)
    leg = ax.legend(fontsize=9, frameon=False, loc="upper right"); leg.get_frame().set_facecolor("none")
    for t in leg.get_texts(): t.set_color(C["ink"])
    ax.set_title("Forecast error by model and horizon, walk-forward split 2024-05", fontsize=10, pad=12, loc="left")
    style(ax)
    save("p4_ablation.png", fig)

def chart_p5():
    sys.path.insert(0, str(ROOT / "earnings-call-nlp"))
    import stats.regression as R
    ds = R.build_dataset(); res = R.newey_west(ds)
    terms = ["surprise", "sentiment", "uncertainty"]
    coefs = [res["coef"][t] for t in terms]
    ses = [abs(res["coef"][t] / res["t"][t]) for t in terms]
    ci_lo = [c - 1.96*s for c, s in zip(coefs, ses)]; ci_hi = [c + 1.96*s for c, s in zip(coefs, ses)]
    pvals = [res["p"][t] for t in terms]; sig = [p < 0.05 for p in pvals]
    fig, ax = plt.subplots(figsize=(6, 2.9), dpi=200)
    for i, (lo, hi, c, sg) in enumerate(zip(ci_lo, ci_hi, coefs, sig)):
        col = C["accent"] if sg else C["muted"]
        ax.plot([lo, hi], [i, i], color=col, lw=2.2, solid_capstyle="round")
        ax.plot([c], [i], "o", color=col, ms=7)
        ax.text(min(hi, 1.4) + 0.12, i + 0.30, f"p={pvals[i]:.3f}", fontsize=8.5, color=col, va="center", ha="left")
    ax.axvline(0, color=C["muted"], lw=1, alpha=0.5)
    ax.set_yticks(range(len(terms)), list(terms), fontsize=9)
    ax.invert_yaxis()
    lo = min(min(ci_lo), -1.5); hi = max(max(ci_hi), 1.5)
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Effect on CAR[+1,+5] per 1-unit change in the term, Newey-West 95% CI", fontsize=8.5)
    ax.set_title("Earnings language and post-announcement drift, 160 events", fontsize=10, pad=12, loc="left")
    style(ax, xgrid=True)
    save("p5_forest.png", fig)

def chart_p6():
    import json
    d = json.loads((ROOT / "alpha-report" / "out" / "alpha_note_inputs.json").read_text())
    variants = [("base momentum", d["sharpe"]), ("+ vol de-lever", d["delev_sharpe"]), ("+ surprise overlay", d["overlay_sharpe"])]
    fig, ax = plt.subplots(figsize=(6, 2.6), dpi=200)
    cols = [C["muted"], C["accent"], C["accent2"]]
    b = ax.barh([v[0] for v in variants][::-1], [v[1] for v in variants][::-1], height=0.5, color=cols[::-1])
    for r, v in zip(b, [v[1] for v in variants][::-1]):
        ax.text(v + 0.008, r.get_y() + r.get_height()/2, f"{v:.3f}", va="center", fontsize=10, color=C["ink"])
    ax.axvline(0, color=C["muted"], lw=1, alpha=0.5); ax.set_xlim(0, 0.3)
    ax.set_title("Sharpe across strategy variants, 24-name panel 2019-2025, 25 bps friction", fontsize=10, pad=12, loc="left")
    style(ax); ax.set_yticklabels([v[0] for v in variants][::-1], fontsize=9)
    save("p6_variants.png", fig)

def run_batch(palette, suffix):
    global SFX
    C.clear(); C.update(palette)
    SFX = suffix
    apply_rc(palette)   # set rcParams (text/axis colors) for this theme
    for f in (chart_p1, chart_p2, chart_p3, chart_p4, chart_p5, chart_p6):
        f()
        print(f"  [{palette is LIGHT and 'light' or 'dark'}] wrote", f.__name__ + suffix)

if __name__ == "__main__":
    run_batch(LIGHT, "")
    run_batch(DARK, "-dark")
    import re
    print("charts:", sorted(p.name for p in OUT.glob("*.png")))
