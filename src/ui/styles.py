import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
.stApp{background:#0d1117;font-family:Inter,sans-serif}
section[data-testid=stSidebar]{background:#161b22!important;border-right:1px solid #30363d}
h1,h2,h3{color:#e6edf3!important}
div[data-testid=stMetric]{background:linear-gradient(145deg,#1c2128,#161b22);border:1px solid #30363d;border-radius:10px;padding:14px 18px}
div[data-testid=stMetric] label{color:#8b949e!important;font-size:.75rem!important;text-transform:uppercase}
div[data-testid=stMetric] div[data-testid=stMetricValue]{color:#e6edf3!important;font-family:'JetBrains Mono',monospace!important;font-size:1.5rem!important}
.stButton>button{background:linear-gradient(135deg,#f0a500,#c48a00)!important;color:#0d1117!important;border:none!important;border-radius:6px!important;font-weight:600!important}
.stTabs [aria-selected=true]{background:#1c2128!important;color:#f0a500!important}
.stTextInput>div>div>input,.stSelectbox>div>div{background:#1c2128!important;border:1px solid #30363d!important;color:#e6edf3!important}
.wy-h{background:linear-gradient(90deg,#161b22,#1c2128,#161b22);border:1px solid #30363d;border-radius:12px;padding:18px 26px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}
.wy-logo{font-size:1.4rem;font-weight:700;color:#f0a500;letter-spacing:.08em;text-transform:uppercase}
.wy-sub{color:#8b949e;font-size:.85rem;margin-top:2px}
.wy-ok{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3);padding:5px 12px;border-radius:20px;font-size:.75rem}
.sec{font-size:1.05rem;font-weight:600;color:#e6edf3;border-left:3px solid #f0a500;padding-left:10px;margin:24px 0 12px}
</style>
"""

def css():
    st.markdown(_CSS, unsafe_allow_html=True)