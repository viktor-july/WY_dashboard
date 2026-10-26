import re
from datetime import datetime
import pandas as pd
import numpy as np


def _csv(url, gid="0"):
    sid = re.search(r"/d/([-\w]+)", url).group(1)
    g = re.search(r"gid=(\d+)", url)
    return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid={g.group(1) if g else gid}"


def _num(v):
    try:
        return float(str(v).replace(",", ".").strip())
    except Exception:
        return np.nan


def _date(v):
    for f in ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(v).strip(), f)
        except Exception:
            pass
    return pd.NaT


def _header(raw):
    for i, row in raw.iterrows():
        if any(k in " ".join(map(str, row)).lower() for k in ("hadley", "hope", "date")):
            return i
    return 0


def _mines(df):
    return [
        c for c in df.columns[1:]
        if "event" not in str(c).lower()
        and df[c].map(_num).notna().mean() > 0.5
    ]


def load(url, gid="0"):
    u = _csv(url, gid)
    raw = pd.read_csv(u, header=None, dtype=str)
    df = pd.read_csv(u, header=_header(raw))
    df.columns = [str(c).strip() for c in df.columns]
    dc = df.columns[0]
    df[dc] = df[dc].map(_date)
    df = df.dropna(subset=[dc]).sort_values(dc).reset_index(drop=True)
    mines = _mines(df)
    df[mines] = df[mines].apply(lambda s: s.map(_num))
    return df[[dc] + mines].rename(columns={dc: "Date"}).dropna(how="all", subset=mines), mines