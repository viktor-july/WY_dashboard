import streamlit as st


def _url():
    return st.text_input("Spreadsheet URL", placeholder="https://docs.google.com/spreadsheets/d/...")


def _gid():
    return st.text_input("Data GID (optional)", value="").strip() or "0"


def _load_btn():
    return st.button("Load / Refresh", use_container_width=True)


def _params():
    return dict(
        iqr_k=st.slider("IQR k", 1.0, 3.0, 1.5, 0.1),
        z_thr=st.slider("Z threshold", 2.0, 5.0, 3.0, 0.1),
        ma_w=st.slider("MA window", 3, 21, 7),
        ma_pct=st.slider("MA %", 10.0, 80.0, 25.0, 5.0),
        alpha=st.select_slider("Grubbs α", [0.01, 0.025, 0.05, 0.1], 0.05),
    )


def _chart_opts():
    kind = st.selectbox("Type", ["Line", "Bar", "Stacked Area"])
    degree = st.selectbox("Trend degree", [0, 1, 2, 3, 4],
                          format_func=lambda x: "None" if x == 0 else str(x))
    return kind, degree


def sidebar():
    with st.sidebar:
        st.markdown("### Data Source")
        url, gid, btn = _url(), _gid(), _load_btn()
        st.markdown("---\n### Anomaly Params")
        params = _params()
        st.markdown("---\n### Chart")
        kind, degree = _chart_opts()
    return url, gid, params, kind, degree, btn