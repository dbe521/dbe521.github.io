# -*- coding: utf-8 -*-
"""contact_sheet.py · 把 14 张界面图拼成一张总览图，便于一次过审

输出：/Users/tk/WorkBuddy/2026-09-20-13-24-26/outputs/样张/14张界面图总览.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.abspath(os.path.join(HERE, "..", "assets", "img"))
OUT = "/Users/tk/WorkBuddy/2026-09-20-13-24-26/outputs/样张/14张界面图总览.png"

ORDER = [
    ("ai-finance-overview", "01 AI 财务超级助理 · 经营总览"),
    ("ai-finance-detail", "01b AI 财务超级助理 · 单据详情"),
    ("project-management-overview", "02 AI 项目成交推进系统 · 项目总览"),
    ("project-management-detail", "02b AI 项目成交推进系统 · 项目详情"),
    ("business-workbench-overview", "03 AI 企业经营决策中心 · 经营驾驶舱"),
    ("business-workbench-detail", "03b AI 企业经营决策中心 · 指标下钻"),
    ("print-control-overview", "04 智能打印管控 · 打印概览"),
    ("print-control-detail", "04b 智能打印管控 · 留底检索与审批"),
    ("meter-billing-overview", "05 智能抄表及账单系统 · 抄表总览"),
    ("meter-billing-detail", "05b 智能抄表及账单系统 · 账单明细"),
    ("service-management-overview", "06 智能售后服务管理 · 服务调度"),
    ("service-management-detail", "06b 智能售后服务管理 · 工单详情"),
    ("ai-customer-service-overview", "07 AI 智能客服 · 客服工作台"),
    ("ai-customer-service-detail", "07b AI 智能客服 · 知识库运营"),
]

COLS = 3
TW, TH = 860, 538          # 缩略图尺寸（16:10）
GAP = 24
LABEL_H = 40
BG = (20, 22, 27)
FG = (226, 232, 240)
SUB = (128, 137, 150)

FONT = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_B = "/System/Library/Fonts/PingFang.ttc"


def font(size, bold=False):
    for p in ([FONT_B] if bold else [FONT]) + [FONT_B, FONT]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


rows = (len(ORDER) + COLS - 1) // COLS
cell_w = TW
cell_h = TH + LABEL_H
W = COLS * cell_w + (COLS + 1) * GAP
H = rows * cell_h + (rows + 1) * GAP + 96

sheet = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(sheet)

# 标题
d.text((GAP + 4, 34), "AI 业务场景 · 14 张系统界面示意图（深色版）", font=font(40, True), fill=FG)
d.text((GAP + 4, 82), "每行左起：概览页 → 明细页。单张原图 2800×1750，见 assets/img/ 目录。",
       font=font(24), fill=SUB)

for i, (name, label) in enumerate(ORDER):
    r, c = i // COLS, i % COLS
    x = GAP + c * (cell_w + GAP)
    y = 96 + GAP + r * (cell_h + GAP)
    p = os.path.join(IMG, name + ".webp")
    if not os.path.exists(p):
        p = os.path.join(IMG, name + ".png")
    if not os.path.exists(p):
        d.rectangle([x, y, x + TW, y + TH], fill=(40, 44, 52))
        d.text((x + 16, y + 16), "缺失: " + name, font=font(22), fill=(240, 120, 120))
        continue
    im = Image.open(p).convert("RGB").resize((TW, TH), Image.LANCZOS)
    sheet.paste(im, (x, y))
    d.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(52, 58, 68), width=1)
    d.text((x + 2, y + TH + 10), label, font=font(25, True), fill=FG)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
sheet.save(OUT)
print("总览图:", OUT)
print("尺寸:", sheet.size, "| %.1f MB" % (os.path.getsize(OUT) / 1048576.0))
