# -*- coding: utf-8 -*-
"""_new08.py · 08 / 08b 智能费控报销（v3 新增）

定位：费用报销 + 采购请款两类单据，规则化审批链、进度全员可见、支付回单留痕，
付款结果直通 AI 财务超级助理的流水底账。不出现 AI 预审表述。
"""

from gen_lib import (
    ic, tag, kpis, panel, chip, table, donut, bar_chart, legend_inline,
    stat_row, timeline,
)

NOTE_TS = "数据更新于 2026-10-27 11:20"


def tb_right(period, name, role, badge="6"):
    return (
        '<div class="tb-pill">%s%s%s</div>'
        '<div class="tb-ic">%s<b>%s</b></div>'
        '<div class="tb-user"><span class="av">%s</span><u>%s · %s</u></div>'
        % (ic("calendar", 13), period, ic("chevron-down", 12),
           ic("bell", 15), badge, name[:2], name, role)
    )


def meta3(items):
    """三列字段网格：[(标签, 值)]"""
    return '<div class="meta3">%s</div>' % "".join(
        '<div><div class="k">%s</div><div class="v">%s</div></div>' % (k, v)
        for k, v in items
    )


def flow_nodes(nodes):
    """横向审批流：[(状态, 名称, 说明)]  状态 done / now / todo"""
    out = []
    for i, (st, name, desc) in enumerate(nodes):
        mark = {"done": "✓", "now": "●", "todo": ""}.get(st, "")
        out.append(
            '<div style="display:flex;align-items:center;flex:1;min-width:0">'
            '<div style="display:flex;align-items:flex-start;gap:9px;min-width:0">'
            '<span class="fdot %s">%s</span>'
            '<div style="min-width:0"><div class="fname">%s</div>'
            '<div class="fdesc">%s</div></div></div>%s</div>'
            % (st, mark, name, desc,
               '<span class="fline"></span>' if i < len(nodes) - 1 else "")
        )
    return '<div class="flownodes">%s</div>' % "".join(out)


def files(items):
    """附件列表：[(扩展名, 文件名, 大小)]"""
    return '<div class="filelist">%s</div>' % "".join(
        '<div class="file"><span class="fext">%s</span>'
        '<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">%s</span>'
        '<span class="mono" style="color:var(--s-t3);font-size:11px">%s</span></div>'
        % (ext, name, size)
        for ext, name, size in items
    )


# ---------------------------------------------------------------- 导航与顶栏

EC_NAV = [
    ("费控工作台", ""), ("待我审批", "6"), ("全部单据", ""),
    ("费用报销", ""), ("采购请款", ""), ("出纳付款", "5"),
    ("报表统计", ""), ("审批流配置", ""), ("#分析", ""),
    ("支出分析", ""), ("通知与日志", ""),
]
EC_F = '<span>本月 48.6 万</span><span class="tag ok">已付 38.6 万</span>'
EC_TB = tb_right("2026 年 10 月", "王芳", "财务主管")

# ---------------------------------------------------------------- 概览数据

APPROVE_COLS = [
    ("单号", 17, ""), ("类型", 12, ""), ("申请人", 10, ""),
    ("金额（元）", 12, "num"), ("当前节点", 21, ""), ("已停留", 10, ""),
    ("状态", 16, ""),
]
APPROVE_ROWS = [
    ["BX-20261027-0012", tag("费用报销", "info"), "李娜", "4,100",
     "老板审批 <span class=\"mono\" style=\"color:var(--s-t3)\">2/4</span>", "6 小时", tag("待老板审批", "warn")],
    ["QK-20261027-0005", tag("采购请款", "acc"), "Winnie", "18,400",
     "老板审批 <span class=\"mono\" style=\"color:var(--s-t3)\">2/4</span>", "4 小时", tag("待老板审批", "warn")],
    ["BX-20261027-0008", tag("费用报销", "info"), "陈静", "1,680",
     "财务复核 <span class=\"mono\" style=\"color:var(--s-t3)\">3/4</span>", "2 小时", tag("待财务复核", "info")],
    ["QK-20261026-0011", tag("采购请款", "acc"), "张伟", "26,800",
     "财务复核 <span class=\"mono\" style=\"color:var(--s-t3)\">3/4</span>", "1 天", tag("待财务复核", "info")],
    ["BX-20261026-0007", tag("费用报销", "info"), "周敏", "860",
     "出纳付款 <span class=\"mono\" style=\"color:var(--s-t3)\">4/4</span>", "3 小时", tag("待付款", "ok")],
    ["QK-20261026-0003", tag("采购请款", "acc"), "李娜", "12,800",
     "出纳付款 <span class=\"mono\" style=\"color:var(--s-t3)\">4/4</span>", "5 小时", tag("待付款", "ok")],
    ["QK-20261025-0012", tag("采购请款", "acc"), "陈静", "6,800",
     "已驳回", "—", tag("已驳回", "bad")],
]

S08 = dict(
    id="08-expense-control",
    name="AI 费控报销系统",
    en="EXPENSE & PURCHASE CONTROL",
    nav=EC_NAV, active="费控工作台",
    crumb="费控工作台 <em>/ 报销与请款总览</em>",
    tb=EC_TB, side_f=EC_F, note=NOTE_TS,
    canvas=(
        kpis([
            dict(label="待我审批", value="6", unit="单", tone="acc",
                 desc="其中 <b>1 单</b>停留超 2 天 · 已催办"),
            dict(label="本月已付", value="38.6", unit="万", tone="ok",
                 desc="付款 42 笔 · 报销与请款合并口径"),
            dict(label="在途单据", value="19", unit="张", tone="warn",
                 desc="费用报销 11 · 采购请款 8"),
            dict(label="平均审批时长", value="4.6", unit="小时", tone="ok",
                 desc="目标 8 小时内 · 本周达标 94%"),
        ]),
        '<div class="row" style="grid-template-columns:minmax(0,2.15fr) minmax(0,1fr)">'
        + panel("待我审批", table(APPROVE_COLS, APPROVE_ROWS, compact=True),
                sub="每一行都标出当前节点与停留时长",
                right=chip("按类型筛选", "filter") + chip("只看超时", "alert-triangle"))
        + panel("本月支出构成", (
            donut([
                ("#F2665B", 46.0, "采购货款", "22.4 万"),
                ("#60A5FA", 21.0, "差旅", "10.2 万"),
                ("#FBBF24", 14.0, "办公用品", "6.8 万"),
                ("#34D399", 11.0, "客户招待", "5.4 万"),
                ("#737B8B", 8.0, "其他", "3.8 万"),
            ], "48.6", "万元 · 本月")
        ), sub="按费用类型 · 含税")
        + "</div>",
        '<div class="row" style="grid-template-columns:minmax(0,1.62fr) minmax(0,1fr)">'
        + panel("近 6 周已付金额", bar_chart(
            ["第 1 周", "第 2 周", "第 3 周", "第 4 周", "第 5 周", "第 6 周"],
            [8.6, 11.2, 7.4, 13.8, 9.6, 12.4],
            ["16", "12", "8", "4", "0"], vmax=16, color="#F2665B"),
            sub="单位：万元", right=chip("查看付款台账", "list-details"),
            cls="panel-h242")
        + panel("审批时效", (
            stat_row([("平均审批", "4.6", "小时"), ("平均付款", "1.2", "天")])
            + '<div style="padding:0 16px 6px">' + "".join(
                '<div class="trow"><span>%s</span><span class="mono">%s</span></div>' % (k, v)
                for k, v in [
                    ("超 2 天未处理", "1 单"),
                    ("本周驳回", "2 单"),
                ]
            ) + "</div>"
        ), sub="超时单自动提醒审批人", cls="panel-h242")
        + "</div>",
    ),
)

# ---------------------------------------------------------------- 明细数据

DETAIL_ITEMS = [
    ["差旅费", "广州出差 2 天 · 高铁往返", "2,860", "高铁票 2 张"],
    ["客户招待", "重点客户 3 人 · 业务洽谈", "1,240", "餐饮发票 1 张"],
]
APPROVAL_NODES = [
    ("done", "提交", "李娜 · 10-27 09:12"),
    ("now", "老板审批", "周明远 · 已等待 6 小时"),
    ("todo", "财务复核", "王芳"),
    ("todo", "出纳付款", "刘敏"),
]
LOGS = [
    ("ok", "李娜 提交单据", "2026-10-27 09:12 · 附发票 3 份"),
    ("acc", "系统自动匹配审批链", "2026-10-27 09:12 · 金额 ≥ 2,000 加老板终审"),
    ("mute", "周明远 待审批", "已等待 6 小时 · 系统已提醒 1 次"),
    ("mute", "财务复核 · 王芳", "老板通过后自动流转"),
    ("mute", "出纳付款 · 刘敏", "付款后回单归档，进入付款台账"),
]

S08B = dict(
    id="08b-expense-detail",
    name="AI 费控报销系统",
    en="EXPENSE & PURCHASE CONTROL",
    nav=EC_NAV, active="待我审批",
    crumb="待我审批 <em>/ BX-20261027-0012</em>",
    tb=EC_TB, side_f=EC_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:84px minmax(0,1fr);gap:16px">'
        # 摘要条
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px">'
        '<span class="tilemark">' + ic("receipt", 20) + "</span>"
        '<div style="margin-left:14px;min-width:0">'
        '<div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">费用报销单 BX-20261027-0012</div>'
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        "李娜 · 渠道部 · 提交于 2026-10-27 09:12</div></div>"
        '<div style="margin-left:26px;display:flex;gap:8px">'
        + chip("费用报销", "receipt") + chip("现款", "wallet") + chip("附件 3 份", "file-invoice")
        + "</div>"
        '<div style="margin-left:auto;display:flex;align-items:center;gap:16px">'
        '<div style="text-align:right"><div style="font-size:10.5px;color:var(--s-t3);letter-spacing:.06em">报销金额</div>'
        '<div class="mono" style="font-size:23px;font-weight:600;letter-spacing:-.02em">¥4,100.00</div></div>'
        + tag("待老板审批", "warn") +
        "</div></div>",
        # 主体
        '<div class="row" style="grid-template-columns:minmax(0,1fr) 348px;grid-template-rows:minmax(0,1fr)">'
        '<div style="display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;gap:14px;min-height:0;height:100%">'
        + panel("审批流", flow_nodes(APPROVAL_NODES),
                sub="单号 BX-20261027-0012", right=chip("当前停留 6 小时", "clock"))
        + panel("单据信息", meta3([
            ("申请人", "李娜"), ("部门", "渠道部"), ("结算方式", "现款"),
            ("收款人", "李娜"), ("收款账号", "<span class=\"mono\">6222 **** 7766</span>"),
            ("开户行", "招商银行"), ("费用归属", "渠道部 · 华南区"),
            ("关联项目", "—"), ("提交时间", "<span class=\"mono\">10-27 09:12</span>"),
        ]), sub="")
        + panel("费用明细",
                table([("费用项", 16, ""), ("说明", 40, ""), ("金额（元）", 14, "num"),
                       ("票据", 30, "")],
                      [[r[0], r[1], r[2], r[3]] for r in DETAIL_ITEMS]
                      + [["<b>合计</b>", "共 2 项", "<b>4,100</b>", "票据 3 张"]], compact=True),
                sub="金额与票据逐项对应")
        + panel("附件", (
            '<div class="filechips">'
            + "".join(
                '<span class="fchip"><b>%s</b>%s<span class="mono">%s</span></span>' % it
                for it in [
                    ("JPG", "高铁票-广州往返.jpg", "820 KB"),
                    ("PDF", "住宿发票-广州.pdf", "360 KB"),
                    ("JPG", "餐饮发票-招待.jpg", "520 KB"),
                ]
            )
            + "</div>"
        ), sub="共 3 份 · 与明细逐项对应")
        + "</div>",
        # 右栏
        '<div style="display:grid;grid-template-rows:auto minmax(0,1fr);gap:14px;min-height:0;height:100%">'
        + panel("审批操作", (
            '<div style="padding:0 16px 16px">'
            '<div style="display:flex;gap:10px;margin-bottom:12px">'
            '<span class="abtn p">' + ic("check", 15) + "通过</span>"
            '<span class="abtn g">' + ic("x", 15) + "驳回</span></div>"
            '<div class="opinion"><div class="opinion-k">审批意见</div>'
            '<div class="opinion-b">同意，票据齐全，与出差申请一致。</div></div>'
            "</div>"
        ), sub="驳回须填原因 · 结果即时通知")
        + panel("流转记录", timeline(LOGS), sub="全程留痕 · 可追溯")
        + "</div>"
        "</div>"
        "</div>"
    ),
)
