import streamlit as st
import pandas as pd


def _kpi_cards(s):
    a, b, c, d = st.columns(4)
    a.metric("Mean", f"{s['mean']:.1f}")
    b.metric("Std", f"{s['std']:.1f}")
    c.metric("Median", f"{s['median']:.1f}")
    d.metric("IQR", f"{s['iqr']:.1f}")


def _kpi_caption(ct):
    st.caption(
        f"Anomalies · IQR:{ct['iqr']} Z:{ct['zscore']} "
        f"MA:{ct['ma']} Grubbs:{ct['grubbs']} Unique:{ct['union']}"
    )


def kpis(names, st_map, anoms):
    st.markdown('<div class="sec">Key Performance Indicators</div>', unsafe_allow_html=True)
    for tab, n in zip(st.tabs([("TOTAL" if n == "TOTAL" else n) for n in names]), names):
        with tab:
            _kpi_cards(st_map[n])
            _kpi_caption(anoms[n]["counts"])


def _overview_table(names, anoms):
    rows = [{"Mine": n, **anoms[n]["counts"]} for n in names]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _flag_table(df, n, mask):
    t = df.loc[mask, ["Date", n]].copy()
    t.columns = ["Date", "Value"]
    t["Date"] = t["Date"].dt.strftime("%d.%m.%Y")
    st.dataframe(t, use_container_width=True, hide_index=True)


def _method_tab(names, df, anoms, key):
    for n in names:
        mask = anoms[n]["flags"][key]
        if not mask.any():
            st.caption(f"{n}: none")
            continue
        with st.expander(f"{n} — {int(mask.sum())}", expanded=(n == "TOTAL")):
            _flag_table(df, n, mask)


def anomalies_ui(names, df, anoms):
    st.markdown('<div class="sec">Anomaly Detection</div>', unsafe_allow_html=True)
    tabs = st.tabs(["Overview", "IQR", "Z-Score", "MA", "Grubbs"])
    with tabs[0]:
        _overview_table(names, anoms)
    for tab, key in zip(tabs[1:], ("iqr", "zscore", "ma", "grubbs")):
        with tab:
            _method_tab(names, df, anoms, key)