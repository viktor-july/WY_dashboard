import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _style():
    plt.rcParams.update({
        "figure.facecolor": "#0d1117",
        "axes.facecolor": "#161b22",
        "axes.edgecolor": "#30363d",
        "axes.labelcolor": "#8b949e",
        "text.color": "#e6edf3",
        "xtick.color": "#8b949e",
        "ytick.color": "#8b949e",
        "grid.color": "#21262d",
        "legend.facecolor": "#161b22",
        "legend.edgecolor": "#30363d",
    })


def _to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def mine_chart(df, mines, title="Daily Extraction by Mine"):
    _style()
    fig, ax = plt.subplots(figsize=(10, 4))
    for m in mines:
        ax.plot(df["Date"], df[m], label=m, linewidth=1.5)
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=7)
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    return _to_bytes(fig)


def total_chart(df, title="Total Extraction"):
    _style()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Date"], df["TOTAL"], color="#f0a500", linewidth=2)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    return _to_bytes(fig)
