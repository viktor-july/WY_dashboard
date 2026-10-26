import numpy as np
import plotly.express as px


def _trend(y, degree):
    x = np.arange(len(y))
    m = ~np.isnan(y)
    if m.sum() <= degree:
        return np.full_like(y, np.nan, dtype=float)
    return np.polyval(np.polyfit(x[m], y[m], degree), x)


def _base(df, mines, kind, title):
    if kind == "Stacked Area":
        return px.area(df, x="Date", y=mines, title=title)
    if kind == "Bar":
        return px.bar(df, x="Date", y=mines, barmode="group", title=title)
    return px.line(df, x="Date", y=mines, title=title)


def _add_trend(fig, df, mine, degree):
    fig.add_scatter(
        x=df["Date"], y=_trend(df[mine].values.astype(float), degree),
        mode="lines", line=dict(dash="dash", width=1.5),
        showlegend=False, hoverinfo="skip",
    )


def _add_outliers(fig, df, mine, mask):
    fig.add_scatter(
        x=df.loc[mask, "Date"], y=df.loc[mask, mine],
        mode="markers", marker=dict(size=10, color="#f85149", symbol="x"),
        showlegend=False, name="outlier",
    )


def _style(fig):
    fig.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#161b22",
        font_color="#8b949e", title_font_color="#e6edf3",
        legend=dict(bgcolor="rgba(22,27,34,0.8)"),
        margin=dict(l=40, r=20, t=50, b=40), height=480,
    )
    return fig


def chart(df, mines, kind="Line", degree=0, masks=None, title=""):
    fig = _base(df, mines, kind, title)
    masks = masks or {}
    for m in mines:
        if degree > 0:
            _add_trend(fig, df, m, degree)
        if m in masks and masks[m].any():
            _add_outliers(fig, df, m, masks[m])
    return _style(fig)