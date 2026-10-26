from datetime import datetime
import streamlit as st
from src.data import load
from src.analysis import stats
from src.analysis.anomalies import detect_all
from src.viz import chart
from src.report import pdf
from src.report.images import mine_chart, total_chart
from src.ui import css, sidebar, kpis, anomalies_ui


def _header():
    st.markdown(
        '<div class="wy-h"><div><div class="wy-logo">Weyland-Yutani</div>'
        '<div class="wy-sub">Resource Extraction Command Dashboard</div></div>'
        '<div class="wy-ok">● ONLINE</div></div>',
        unsafe_allow_html=True,
    )


def _init():
    st.set_page_config(page_title="Weyland-Yutani | Extraction", page_icon="⛏️", layout="wide")
    css()
    _header()
    if "df" not in st.session_state:
        st.session_state.df = st.session_state.mines = None


def _try_load(url, gid):
    try:
        df, mines = load(url, gid)
        if df is None or df.empty or not mines:
            st.error("Loaded 0 days / 0 mines. Check that the Data sheet is public and the GID is correct.")
            return
        st.session_state.df, st.session_state.mines = df, mines
        st.success(f"Loaded {len(df)} days · {len(mines)} mines: {', '.join(mines[:4])}{'…' if len(mines)>4 else ''}")
    except Exception as e:
        st.error(str(e))
        st.info("Tips: 1) Share sheet as Anyone with the link can view. 2) Open the Data tab and copy its gid= from the URL.")


def _select_mines(mines):
    st.markdown('<div class="sec">Mines</div>', unsafe_allow_html=True)
    return st.multiselect("mines", mines, mines, label_visibility="collapsed")


def _prepare(df, sel, params):
    work = df.copy()
    work["TOTAL"] = work[sel].sum(axis=1)
    cols = sel + ["TOTAL"]
    st_map = {c: stats(work[c]) for c in cols}
    anoms = detect_all(work, cols, **params)
    return work, cols, st_map, anoms


def _fig_main(work, sel, anoms, kind, degree):
    masks = {m: anoms[m]["union"] for m in sel}
    return chart(work, sel, kind, degree, masks, "Daily Extraction by Mine")


def _fig_total(work, anoms, kind, degree):
    k = "Line" if kind == "Stacked Area" else kind
    return chart(work, ["TOTAL"], k, degree,
                 {"TOTAL": anoms["TOTAL"]["union"]}, "Total Extraction")


def _show_charts(work, sel, anoms, kind, degree):
    st.markdown('<div class="sec">Charts</div>', unsafe_allow_html=True)
    fig1 = _fig_main(work, sel, anoms, kind, degree)
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = _fig_total(work, anoms, kind, degree)
    st.plotly_chart(fig2, use_container_width=True)
    return fig1, fig2


def _raw(work, sel):
    with st.expander("Raw data"):
        p = work[["Date"] + sel + ["TOTAL"]].copy()
        p["Date"] = p["Date"].dt.strftime("%d.%m.%Y")
        st.dataframe(p, use_container_width=True, hide_index=True)


def _make_imgs(work, sel):
    return [
        (mine_chart(work, sel), "By mine"),
        (total_chart(work), "Total"),
    ]


def _pdf_section(work, sel, st_map, anoms, params):
    st.markdown('<div class="sec">Report</div>', unsafe_allow_html=True)
    if not st.button("Generate PDF", use_container_width=True):
        return
    try:
        buf = pdf(work, sel, st_map, anoms, _make_imgs(work, sel), params)
        st.download_button(
            "Download PDF", buf,
            f"WY_Report_{datetime.now():%Y%m%d_%H%M}.pdf",
            "application/pdf", use_container_width=True,
        )
    except Exception as e:
        st.error(f"PDF failed: {e}")


def _body(df, mines, params, kind, degree):
    sel = _select_mines(mines)
    if not sel:
        return
    work, cols, st_map, anoms = _prepare(df, sel, params)
    kpis(cols, st_map, anoms)
    fig1, fig2 = _show_charts(work, sel, anoms, kind, degree)
    anomalies_ui(cols, work, anoms)
    _raw(work, sel)
    _pdf_section(work, sel, st_map, anoms, params)


def main():
    _init()
    url, gid, params, kind, degree, do_load = sidebar()
    if do_load and url:
        _try_load(url, gid)
    df, mines = st.session_state.df, st.session_state.mines
    if df is None:
        st.info("Paste spreadsheet URL and click Load.")
        return
    _body(df, mines, params, kind, degree)


if __name__ == "__main__":
    main()
