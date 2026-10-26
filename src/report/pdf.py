import io
from datetime import datetime
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(240, 165, 0)
        self.cell(0, 10, "WEYLAND-YUTANI CORPORATION", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, self._subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "Weyland-Yutani - Building Better Worlds", align="C")


def _hdr_row(pdf, headers, col_w):
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(28, 33, 40)
    pdf.set_text_color(240, 165, 0)
    for h, w in zip(headers, col_w):
        pdf.cell(w, 7, str(h), border=1, fill=True, align="C")
    pdf.ln()


def _data_row(pdf, row, col_w, fill):
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 30, 30)
    pdf.set_fill_color(*fill)
    for val, w in zip(row, col_w):
        pdf.cell(w, 6, str(val), border=1, fill=True, align="C")
    pdf.ln()


def _table(pdf, headers, rows, col_w):
    _hdr_row(pdf, headers, col_w)
    for i, row in enumerate(rows):
        fill = (245, 240, 224) if i == 0 else (255, 255, 255)
        _data_row(pdf, row, col_w, fill)


def _stats_rows(mines, st):
    return [
        [m, f"{st[m]['mean']:.1f}", f"{st[m]['std']:.1f}",
         f"{st[m]['median']:.1f}", f"{st[m]['iqr']:.1f}", st[m]["n"]]
        for m in ["TOTAL"] + mines
    ]


def _stats_block(pdf, mines, st):
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "1. Summary Statistics", new_x="LMARGIN", new_y="NEXT")
    _table(pdf, ["Mine", "Mean", "Std", "Median", "IQR", "N"],
           _stats_rows(mines, st), [40, 28, 28, 28, 28, 20])
    pdf.ln(4)


def _anom_rows(mines, anoms):
    return [
        [m, anoms[m]["counts"]["iqr"], anoms[m]["counts"]["zscore"],
         anoms[m]["counts"]["ma"], anoms[m]["counts"]["grubbs"],
         anoms[m]["counts"]["union"]]
        for m in ["TOTAL"] + mines
    ]


def _anom_block(pdf, mines, anoms):
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "3. Anomalies Overview", new_x="LMARGIN", new_y="NEXT")
    _table(pdf, ["Mine", "IQR", "Z", "MA", "Grubbs", "Unique"],
           _anom_rows(mines, anoms), [40, 25, 25, 25, 30, 25])
    pdf.ln(4)


def _detail_row(d, mean):
    return [
        d["date"].strftime("%d.%m.%Y"), f"{d['value']:.1f}",
        "Y" if d["iqr"] else "", "Y" if d["zscore"] else "",
        "Y" if d["ma"] else "", "Y" if d["grubbs"] else "",
        "SPIKE" if d["value"] > mean else "DROP",
    ]


def _one_mine_details(pdf, m, dets, mean):
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(192, 57, 43)
    pdf.cell(0, 7, m, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    rows = [_detail_row(d, mean) for d in sorted(dets, key=lambda x: x["date"])]
    _table(pdf, ["Date", "Value", "IQR", "Z", "MA", "Grubbs", "Type"],
           rows, [28, 22, 18, 18, 18, 22, 22])
    pdf.ln(3)


def _details_block(pdf, mines, anoms, st):
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "4. Anomaly Details", new_x="LMARGIN", new_y="NEXT")
    for m in mines:
        if anoms[m]["details"]:
            _one_mine_details(pdf, m, anoms[m]["details"], st[m]["mean"])


def _charts_block(pdf, images):
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "2. Charts", new_x="LMARGIN", new_y="NEXT")
    for img_bytes, cap in images:
        pdf.image(io.BytesIO(img_bytes), w=180)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 5, cap, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)


def _params_line(pdf, params):
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(
        0, 5,
        f"IQR k={params['iqr_k']} | Z={params['z_thr']} | "
        f"MA={params['ma_w']}d/{params['ma_pct']}% | a={params['alpha']}",
        new_x="LMARGIN", new_y="NEXT",
    )
    pdf.ln(3)


def _new_doc(df):
    doc = PDF()
    doc._subtitle = (
        f"Extraction Report - {datetime.now():%Y-%m-%d %H:%M} - "
        f"{df['Date'].min():%d.%m.%Y} - {df['Date'].max():%d.%m.%Y}"
    )
    return doc


def _page1(doc, mines, st, params, images):
    doc.add_page()
    _stats_block(doc, mines, st)
    _params_line(doc, params)
    _charts_block(doc, images)


def _page2(doc, mines, anoms, st):
    doc.add_page()
    _anom_block(doc, mines, anoms)
    _details_block(doc, mines, anoms, st)


def pdf(df, mines, st, anoms, images, params):
    doc = _new_doc(df)
    _page1(doc, mines, st, params, images)
    _page2(doc, mines, anoms, st)
    buf = io.BytesIO()
    doc.output(buf)
    buf.seek(0)
    return buf
