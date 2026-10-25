# -*- coding: utf-8 -*-
"""使用说明.md → 使用说明.pdf（fpdf2 + 微软雅黑，手写轻量渲染）"""
import re
from fpdf import FPDF

SRC = r"E:\allthings\mcd\mcd-profiler\docs\使用说明.md"
OUT = r"E:\allthings\mcd\mcd-profiler\docs\使用说明.pdf"

GREEN = (63, 185, 80)
ORANGE = (240, 136, 62)
DARK = (30, 35, 42)
DIM = (110, 118, 128)
CODE_BG = (13, 17, 23)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("yh", "", r"C:\Windows\Fonts\msyh.ttc")
        self.add_font("yh", "B", r"C:\Windows\Fonts\msyhbd.ttc")
        self.set_auto_page_break(True, margin=18)
        self.W = self.w - self.l_margin - self.r_margin

    def header(self):
        if self.page_no() > 1:
            self.set_font("yh", "", 8)
            self.set_text_color(*DIM)
            self.cell(0, 6, "麦门侧写师 McProfiling · 使用说明", align="R")
            self.ln(8)

    def footer(self):
        self.set_y(-14)
        self.set_font("yh", "", 8)
        self.set_text_color(*DIM)
        self.cell(0, 8, f"第 {self.page_no()} 页", align="C")

pdf = PDF()
pdf.add_page()

def h1(text):
    pdf.set_font("yh", "B", 20); pdf.set_text_color(*DARK)
    pdf.ln(2); pdf.cell(0, 12, text); pdf.ln(2)
    pdf.set_draw_color(*GREEN); pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y()); pdf.ln(5)

def h2(text):
    pdf.ln(4); pdf.set_font("yh", "B", 14); pdf.set_text_color(*ORANGE)
    pdf.cell(0, 9, text); pdf.ln(11)

def h3(text):
    pdf.ln(2); pdf.set_font("yh", "B", 11.5); pdf.set_text_color(*DARK)
    pdf.cell(0, 8, text); pdf.ln(9)

def para(text, bold=False, size=10.5):
    pdf.set_font("yh", "B" if bold else "", size); pdf.set_text_color(*DARK)
    pdf.multi_cell(pdf.W, 6.2, text); pdf.ln(1.5)

def quote(text):
    y = pdf.get_y()
    pdf.set_fill_color(234, 244, 236)
    pdf.set_draw_color(*GREEN)
    pdf.set_font("yh", "", 10); pdf.set_text_color(50, 90, 60)
    pdf.multi_cell(pdf.W, 6, text, fill=True)
    pdf.set_line_width(1.2)
    pdf.line(pdf.l_margin, y, pdf.l_margin, pdf.get_y())
    pdf.ln(2)

def code(lines):
    pdf.set_font("yh", "", 9)
    lh = 5.2
    h = lh * len(lines) + 6
    if pdf.get_y() + h > pdf.page_break_trigger:
        pdf.add_page()
    x, y = pdf.l_margin, pdf.get_y()
    pdf.set_fill_color(*CODE_BG)
    pdf.rect(x, y, pdf.W, h, "F")
    pdf.set_text_color(63, 185, 80)
    pdf.set_xy(x + 4, y + 3)
    for ln in lines:
        pdf.set_x(x + 4)
        pdf.cell(pdf.W - 8, lh, ln)
        pdf.ln(lh)
    pdf.set_y(y + h + 4)

def table(rows, widths):
    pdf.set_font("yh", "B", 9.5); pdf.set_text_color(*ORANGE)
    pdf.set_draw_color(200, 208, 216)
    for i, row in enumerate(rows):
        pdf.set_font("yh", "B" if i == 0 else "", 9.5)
        pdf.set_text_color(*ORANGE) if i == 0 else pdf.set_text_color(*DARK)
        pdf.set_fill_color(244, 246, 248) if i == 0 else None
        for j, cell in enumerate(row):
            pdf.cell(widths[j], 7, cell, border=1, fill=(i == 0))
        pdf.ln()
    pdf.ln(2)

md = open(SRC, encoding="utf-8").read()
lines = md.split("\n")
i = 0
in_code = False
code_buf = []

def clean(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", s)
    return s

while i < len(lines):
    ln = lines[i]
    if ln.strip().startswith("```"):
        if in_code:
            code(code_buf); code_buf = []; in_code = False
        else:
            in_code = True
        i += 1; continue
    if in_code:
        code_buf.append(ln.rstrip()); i += 1; continue

    if ln.startswith("| ") and i + 1 < len(lines) and lines[i+1].startswith("|--") is False and set(lines[i+1].replace("|", "").replace(" ", "")) <= {"-", ":"} and lines[i+1].startswith("|"):
        rows = [[clean(c).strip() for c in ln.strip("|").split("|")]]
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([clean(c).strip() for c in lines[i].strip("|").split("|")])
            i += 1
        n = len(rows[0])
        widths = [pdf.W / n] * n
        table(rows, widths)
        continue

    if ln.startswith("# "):
        h1(clean(ln[2:]))
    elif ln.startswith("## "):
        h2(clean(ln[3:]))
    elif ln.startswith("### "):
        h3(clean(ln[4:]))
    elif ln.startswith("> "):
        quote(clean(ln[2:]))
    elif ln.startswith("- "):
        para("· " + clean(ln[2:]))
    elif re.match(r"^\d+\. ", ln):
        para(clean(ln))
    elif ln.strip() == "---":
        pdf.ln(3)
        pdf.set_draw_color(220, 224, 228); pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + pdf.W, pdf.get_y())
        pdf.ln(3)
    elif ln.strip():
        para(clean(ln.strip()))
    i += 1

pdf.output(OUT)
print("pdf done:", OUT)
