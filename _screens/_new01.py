# -*- coding: utf-8 -*-
"""_new01.py · 01 / 01b 的案例版重做定义
依据《财务自动化系统 · 上线价值说明与功能讲解（第二版）》案例。
定位：现有财务系统（金蝶/管家婆）+ AI 财务超级助理，补位而非替代。
"""

from gen_lib import (
    ic, tag, kpi, kpis, panel, chip, table, area_chart, legend_inline,
    pipeline, chan_card, timeline, kv,
)

NOTE_TS = "数据更新于 2026-09-03 09:14"


def tb_right(period, name, role, badge="3"):
    return (
        '<div class="tb-pill">%s%s%s</div>'
        '<div class="tb-ic">%s<b>%s</b></div>'
        '<div class="tb-user"><span class="av">%s</span><u>%s · %s</u></div>'
        % (ic("calendar", 13), period, ic("chevron-down", 12),
           ic("bell", 15), badge, name[:2], name, role)
    )


FIN_NAV = [
    ("数据处理总览", ""), ("源文件接入", "2"), ("对手名标准化", ""), ("科目分类", "28"),
    ("核销与账龄", ""), ("对账单分发", ""), ("报表与勾稽", ""), ("人工裁决", "46"),
    ("#系统", ""), ("规则与配置", ""),
]
FIN_F = '<span>本期 M 月 · 800 笔流水</span><span class="tag ok">运行完成</span>'
FIN_TB = tb_right("本期 M 月", "李静", "财务负责人")

# 案例：8 类源文件 → 统一出纳账 → 应收应付底账 → 三大报表 → 对账单
PIPE = [
    ("0", "回读裁决", "写入映射库永久生效"),
    ("1", "解析去重", "8 类源文件归一"),
    ("2", "对手归并", "7 级匹配 · 待校准"),
    ("3", "科目分类", "5 级规则 · 待填写"),
    ("4", "核销账龄", "FIFO · 账龄 · 预警"),
    ("5", "报表输出", "三大报表与底账"),
    ("6", "对账与看板", "对账单 + 离线看板"),
]

BALANCE_COLS = [
    ("资金账户", 25, ""), ("期初", 17, "num"), ("推算期末", 19, "num"),
    ("源内最后余额", 19, "num"), ("余额差异", 20, "num"),
]
BALANCE_ROWS = [
    ["银行账户①", "43,000.00", "140,000.00", "140,000.00", "0.00"],
    ["银行账户②", "86,000.00", "64,000.00", "64,000.00", "0.00"],
    ["银行账户③", "0.00", "0.00", "—", "—"],
    ["个人结算卡", "153,000.00", "47,000.00", "—", "—"],
    ["移动支付账户①", "4,000.00", "2,000.00", "—", "—"],
    ["移动支付账户②", "15,000.00", "43,000.00", "—", "—"],
    ["移动支付账户③", "8,000.00", "6,100.00", "6,350.00", tag("−250.00", "bad")],
    ["电商收款账户①", "25,000.00", "43,000.00", "43,000.00", "0.00"],
    ["电商收款账户②", "20,000.00", "23,000.00", "—", "—"],
    ["电商收款账户③", "2,000.00", "2,000.00", "—", "—"],
    ["<b>合计</b>", "—", "<b>370,100.00</b>", "—", "—"],
]

SRC_COLS = [("源文件类型", 34, ""), ("接入范围", 26, ""), ("完整性校验", 40, "")]
SRC_ROWS = [
    ["银行日记账", "3 个账户", tag("昨日余额与期初一致", "ok")],
    ["平台官方账单", "2 个账户", tag("声明笔数 = 明细行数", "ok")],
    ["平台对账文件", "1 个账户", tag("实为 XML，已正确解析", "ok")],
    ["电商账单", "3 个账户", tag("订单号已写入备注栏", "ok")],
    ["个人卡手工账", "1 个账户", tag("借方流入 / 贷方流出", "ok")],
    ["进销存单据", "销售 + 采购", tag("表头别名自动兼容", "ok")],
    ["期初表", "资金 / 利润 / 资产负债 / 往来", tag("4 类期初已就位", "ok")],
    ["待计提费用表", "其他应收 / 应付", tag("小计行已取", "ok")],
]

S01N = dict(
    id="01-ai-finance-overview", name="AI 财务超级助理", en="AI FINANCE COPILOT",
    nav=FIN_NAV, active="数据处理总览", crumb="数据处理总览 <em>/ 本期运行结果</em>",
    tb=FIN_TB, side_f=FIN_F, note=NOTE_TS,
    canvas=(
        kpis([
            dict(label="本期处理流水", value="800", unit="笔", tone="acc",
                 desc="来自 <b>8 类源文件</b> · 10 个资金账户"),
            dict(label="月结投入", value="1.9", unit="人天", tone="ok",
                 desc="上线前 18 人天 · <i>降幅 89%</i>"),
            dict(label="待人工裁决", value="46", unit="条", tone="warn",
                 desc="待填写 28 · 待校准 18 · 裁决后永久生效"),
            dict(label="出账时点", value="每月 3 号", tone="acc",
                 desc="上线前需到月中才能出表"),
        ]),
        panel("数据处理流水线", pipeline(PIPE),
              sub="双击一次，从原始账单跑到全套报表与对账单",
              right=chip("查看本次运行日志", "history"), cls="panel-h148"),
        '<div class="row" style="grid-template-columns:minmax(0,1.42fr) minmax(0,1fr)">'
        + panel("资金账户余额核对", table(BALANCE_COLS, BALANCE_ROWS, compact=True),
                sub="系统推算期末 与 源文件余额 逐户核对",
                right=chip("差异单列 · 不掩盖 · 不调平", "alert-triangle", True))
        + panel("源文件接入与解析", table(SRC_COLS, SRC_ROWS),
                sub="8 类源文件 · 解析告警 0 条",
                right=chip("数据质量", "file-check"))
        + "</div>"
    ),
)

# ---------------------------------------------------------------- 01b 账实核对与人工裁决闭环

S01BN = dict(
    id="01b-ai-finance-detail", name="AI 财务超级助理", en="AI FINANCE COPILOT",
    nav=FIN_NAV, active="人工裁决", crumb="人工裁决 <em>/ 账实核对与规则沉淀</em>",
    tb=tb_right("本期 M 月", "李静", "财务负责人", "46"),
    side_f=FIN_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px">'
        # 运行快照条
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<span class="tilemark">' + ic("history-toggle", 20) + "</span>"
        '<div style="margin-left:14px">'
        '<div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        "本次运行快照 · 2026-09-03 09:12</div>"
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        "耗时 2 分 14 秒 · 全量中间结果已留档，任何时点的数字都可复现</div></div>"
        '<div style="margin-left:auto;display:flex;align-items:center;gap:22px">'
        + "".join(
            '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">%s</div>'
            "<div style=\"font-size:18px;font-weight:600;font-family:'Geist Mono',monospace;"
            'margin-top:3px">%s</div></div>' % (k, v)
            for k, v in [("处理流水", "800 笔"), ("生成报表", "3 张"),
                         ("对账单", "220 份"), ("待收敛差异", "3 项")]
        )
        + "</div></div>"
        # 两栏
        '<div class="row" style="grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)">'
        # 左：账实核对
        + panel("账实核对", (
            '<div style="padding:0 0 4px">'
            + table(
                [("交叉核对", 34, ""), ("逻辑", 40, ""), ("结果", 26, "")],
                [
                    ["银行「昨日余额」与期初模板", "两个独立来源互相印证", tag("一致", "ok")],
                    ["平台账单声明笔数与明细行数", "检测账单是否导出完整", tag("一致", "ok")],
                    ["系统推算期末与源文件余额", "检验是否漏读 / 多读", tag("1 项差异", "warn")],
                ],
            )
            + "</div>"
            '<div style="border-top:1px solid var(--s-line);margin:0 16px"></div>'
            '<div style="padding:14px 16px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:4px">'
            "待收敛清单（3 项，如实列示不掩盖）</div>"
            + timeline([
                ("warn", "期初往来款整体挂账", "期初表仅有汇总金额、无逐户明细，单列一行且不参与催收预警"),
                ("warn", "应收核销池口径差异", "应收余额只认「分类=销售收入 且 已匹配」的收款，经财务裁定维持"),
                ("bad", "移动支付账户③ 期初差异 −250.00", "期初表登记 8,000.00，源账单余额链反推 8,250.00；按裁定保留期初登记值"),
            ])
            + '<div style="margin:0 16px 14px;padding:11px 13px;'
            'background:var(--s-panel-2);border:1px solid var(--s-line);border-radius:9px;'
            'font-size:11.5px;color:var(--s-t3);line-height:1.65">'
            "差异单列、不掩盖、不调平。每解决一项，差异就收窄一笔，"
            "全部差异项纳入待收敛清单逐项推进，而非抹平。</div>"
            + "</div>"
        ), sub="三处内置交叉核对 · 差异如实列示",
            right=chip("按待收敛清单逐项推进")),
        # 右：人工裁决闭环
        panel("人工裁决闭环", (
            '<div style="padding:14px 16px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:11px">'
            "三个填写通道 · 一次裁决、永久生效</div>"
            + chan_card("通道 A · 出纳账订正列", "12", "条",
                        "《出纳账汇总》黄色三列",
                        "回读后写入映射库，该对手今后同类流水自动匹配")
            + chan_card("通道 B · 分类待填写", "28", "条",
                        "桌面《分类待填写表》",
                        "填写后重跑自动回填，条目从表中消失")
            + chan_card("通道 C · 待校准对手", "18", "条",
                        "桌面《待校准对手填写表》",
                        "认领 / 同名确认 / 忽略 / 按对手指定科目")
            + '<div style="background:rgba(248,113,113,.09);border:1px solid rgba(248,113,113,.3);'
            'border-radius:9px;padding:11px 13px;margin-bottom:14px;font-size:11.5px;'
            'color:#FCA5A5;line-height:1.6">' + ic("alert-triangle", 13)
            + " 填写禁区：电商收款账户下的对手名一律填「忽略」，绝不能填同名 —— "
            "否则收款会从该电商客户名下被移走，连带改动应收余额与全部对账单。</div>"
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:8px">'
            "每月人工干预量（条）· 越用越省力</div>"
            + area_chart(
                [("#22D3EE", 1.8, [186, 124, 88, 63, 52, 46], 0.22, "34,211,238")],
                ["200", "150", "100", "50", "0"],
                [(44, "第 1 月", "start"), (271, "第 2 月", "middle"),
                 (498, "第 3 月", "middle"), (726, "第 4 月", "middle"),
                 (953, "第 5 月", "middle"), (1180, "第 6 月", "end")],
                vmax=200, height=110, top=8)
            + '<div style="font-size:11.5px;color:var(--s-t3);line-height:1.6">'
            "每一次裁决都变成下月运行的规则，自动处理率随之单调上升。</div>"
            "</div>"
        ), sub="一次裁决 · 永久生效",
            right=chip("别名表 142", "database") + chip("规则 86", "database")),
        "</div>"
        "</div>"
    ),
)
