import numpy as np
import pandas as pd
from scipy.stats import t


def _iqr(s, k=1.5):
    q1, q3 = s.quantile([0.25, 0.75])
    return (s < q1 - k * (q3 - q1)) | (s > q3 + k * (q3 - q1))


def _z(s, thr=3.0):
    std = s.std(ddof=1)
    return pd.Series(False, index=s.index) if not std else ((s - s.mean()) / std).abs() > thr


def _ma(s, window=7, pct=25.0):
    m = s.rolling(window, min_periods=1).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        return ((s - m) / m.replace(0, np.nan)).abs() * 100 > pct


def _grubbs_step(w, alpha):
    n, mu, std = len(w), w.mean(), w.std(ddof=1)
    if not std:
        return None
    tc = t.ppf(1 - alpha / (2 * n), n - 2)
    gc = ((n - 1) / np.sqrt(n)) * np.sqrt(tc**2 / (n - 2 + tc**2))
    idx = (w - mu).abs().idxmax()
    return idx if abs(w[idx] - mu) / std > gc else None


def _grubbs(s, alpha=0.05):
    out, w = pd.Series(False, index=s.index), s.dropna().copy()
    while len(w) >= 3:
        idx = _grubbs_step(w, alpha)
        if idx is None:
            break
        out.loc[idx] = True
        w = w.drop(idx)
    return out


def _flags(s, iqr_k, z_thr, ma_w, ma_pct, alpha):
    return {
        "iqr": _iqr(s, iqr_k),
        "zscore": _z(s, z_thr),
        "ma": _ma(s, ma_w, ma_pct),
        "grubbs": _grubbs(s, alpha),
    }


def _details(s, dates, flags, union):
    return [
        {"date": dates[i], "value": float(s[i]), **{k: bool(flags[k][i]) for k in flags}}
        for i in s.index[union]
    ]


def detect(s, dates, iqr_k=1.5, z_thr=3.0, ma_w=7, ma_pct=25.0, alpha=0.05):
    flags = _flags(s, iqr_k, z_thr, ma_w, ma_pct, alpha)
    union = flags["iqr"] | flags["zscore"] | flags["ma"] | flags["grubbs"]
    counts = {k: int(v.sum()) for k, v in flags.items()}
    counts["union"] = int(union.sum())
    return {"flags": flags, "union": union, "counts": counts,
            "details": _details(s, dates, flags, union)}


def detect_all(df, cols, **kw):
    return {c: detect(df[c], df["Date"], **kw) for c in cols}