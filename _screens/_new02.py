# -*- coding: utf-8 -*-
"""_new02.py · 02 / 02b 重做定义

重点展示两件事：
  商机管理（商机漏斗 / 商机统计 / 商机明细）
  项目管理（8 阶段递进看板，突出当前阶段与下一阶段的执行点、关键点）
"""

from gen_lib import (
    ic, tag, kpi, kpis, panel, chip, table, funnel, stage_board, stage_flow,
    timeline, progress_rows, stat_row,
)

NOTE_TS = "数据更新于 2026-09-21 18:40"


def tb_right(period, name, role, badge="3"):
    return (
        '<div class="tb-pill">%s%s%s</div>'
        '<div class="tb-ic">%s<b>%s</b></div>'
        '<div class="tb-user"><span class="av">%s</span><u>%s · %s</u></div>'
        % (ic("calendar", 13), period, ic("chevron-down", 12),
           ic("bell", 15), badge, name[:2], name, role)
    )


PRJ_NAV = [
    ("商机总览", ""), ("商机漏斗", ""), ("商机明细", "47"), ("客户档案", ""),
    ("项目推进看板", "8"), ("方案与报价", ""), ("合同与回款", "3"), ("服务与续约", ""),
    ("#分析", ""), ("赢单与流失分析", ""),
]
PRJ_F = '<span>在跟商机 47 个</span><span class="tag ok">4,860 万</span>'
PRJ_TB = tb_right("2026 年 9 月", "周靖川", "销售总监")

# 8 个阶段：名称 / 组合数量 / 执行点 / 关键点
STAGES = [
    ("客户开发", "18 个 · 1,240 万", "梳理客户名录与需求线索", "判断采购需求与预算窗口"),
    ("客户关系发展", "12 个 · 860 万", "多线对接，摸清决策链", "锁定关键决策人与影响者"),
    ("客户立项", "7 个 · 1,960 万", "推动客户内部立项", "拿到需求确认与预算批复"),
    ("方案提交", "5 个 · 486 万", "输出方案与报价", "需求逐条对齐，报价在预算内"),
    ("方案沟通", "4 个 · 328 万", "方案讲解与答疑", "技术无异议，摸清竞品口径"),
    ("商务及采购对应", "3 个 · 742 万", "商务谈判与招投标流程", "账期与交付边界写入合同"),
    ("消除疑虑及成交", "2 个 · 268 万", "逐项化解最后顾虑", "明确签约时点与首付款"),
    ("实施及交付", "6 个 · 1,860 万", "进场实施与阶段验收", "验收标准前置，回款挂钩验收单"),
]
CUR = 4  # 当前阶段索引（方案沟通）

SJ_COLS = [("商机编号", 15, ""), ("客户", 25, ""), ("金额（万）", 12, "num"),
           ("所处阶段", 17, ""), ("负责人", 11, ""), ("赢单概率", 20, "")]
SJ_ROWS = [
    ["SJ-2609-047", "宁波睿达智能装备", "268", tag("方案沟通", "info"), "周靖川", "<b>75%</b>"],
    ["SJ-2609-041", "苏州工业园区管委会", "1,960", tag("客户立项", "mute"), "吴桐", "45%"],
    ["SJ-2608-036", "杭州海联电子", "486", tag("商务采购", "warn"), "陆铭", "<b>85%</b>"],
    ["SJ-2608-028", "无锡恒信精密", "328", tag("方案沟通", "info"), "周靖川", "70%"],
    ["SJ-2607-019", "合肥创元新材料", "742", tag("消除疑虑", "ok"), "吴桐", "<b>90%</b>"],
    ["SJ-2607-012", "嘉兴瑞光电工", "156", tag("客户关系", "mute"), "陆铭", "35%"],
    ["SJ-2606-008", "绍兴越信纺织", "520", tag("客户开发", "mute"), "周靖川", "20%"],
]

S02N = dict(
    id="02-project-overview", name="AI 项目成交推进系统", en="DEAL PIPELINE & DELIVERY",
    nav=PRJ_NAV, active="商机总览", crumb="商机总览 <em>/ 成交推进全景</em>",
    tb=PRJ_TB, side_f=PRJ_F, note=NOTE_TS,
    canvas=(
        kpis([
            dict(label="在跟商机", value="47", unit="个", tone="acc",
                 desc="商机总额 <b>4,860 万</b> · 平均客单 103 万"),
            dict(label="本月新增商机", value="12", unit="个", tone="ok",
                 desc="其中已立项 <i>5 个</i> · 转化率 19.1%"),
            dict(label="本月成交", value="1,860", unit="万", tone="ok",
                 desc="成交 9 个项目 · 平均周期 68 天"),
            dict(label="阶段停滞预警", value="3", unit="个", tone="warn",
                 desc="单阶段停留 <b>超 30 天</b> · 需推进"),
        ]),
        '<div class="row" style="grid-template-columns:400px minmax(0,1fr)">'
        + panel("商机漏斗", (
            funnel([("线索池", "192 条"),
                    ("有效商机", "47 个 · 4,860 万"),
                    ("方案阶段", "21 个 · 2,640 万"),
                    ("商务阶段", "14 个 · 2,180 万"),
                    ("成交", "9 个 · 1,860 万")])
            + '<div style="border-top:1px solid var(--s-line);margin:0 16px 4px"></div>'
            + stat_row([("平均成交周期", "68", "天"), ("平均客单价", "103", "万")])
            + stat_row([("全周期赢单率", "19.1", "%"), ("平均报价轮次", "2.4", "次")])
        ), sub="线索 → 商机 → 方案 → 商务 → 成交", right=chip("按业务员筛选", "filter"))
        + panel("商机明细", table(SJ_COLS, SJ_ROWS, compact=True),
                sub="按赢单概率排序 · 共 47 个在跟商机",
                right=chip("按阶段筛选", "filter") + chip("导出", "download"))
        + "</div>",
        panel("项目成交推进看板 · 8 个阶段", stage_board(STAGES, CUR),
              sub="当前阶段与下一阶段的执行点、关键点已高亮标注",
              right=chip("切换项目视图", "chevron-down") + chip("只看停滞项目", "alert-triangle"),
              cls="panel-h258"),
    ),
)

# ---------------------------------------------------------------- 02b 单项目阶段详情

FLOW = [
    ("客户开发", "", "梳理客户名录与需求线索", "判断采购需求与预算窗口", "已完成 · 06-30"),
    ("客户关系发展", "", "多线对接，摸清决策链", "锁定关键决策人与影响者", "已完成 · 07-18"),
    ("客户立项", "", "推动客户内部立项", "拿到需求确认与预算批复", "已完成 · 08-06"),
    ("方案提交", "", "输出方案与报价", "需求逐条对齐，报价在预算内", "已完成 · 08-28"),
    ("方案沟通", "", "方案讲解与答疑", "技术无异议，摸清竞品口径", "进行中 · 已 18 天"),
    ("商务及采购对应", "", "商务谈判与招投标流程", "账期与交付边界写入合同", "计划 10-05"),
    ("消除疑虑及成交", "", "逐项化解最后顾虑", "明确签约时点与首付款", "计划 10-15"),
    ("实施及交付", "", "进场实施与阶段验收", "验收标准前置，回款挂钩验收单", "计划 11-20"),
]

S02BN = dict(
    id="02b-project-detail", name="AI 项目成交推进系统", en="DEAL PIPELINE & DELIVERY",
    nav=PRJ_NAV, active="项目推进看板", crumb="项目推进看板 <em>/ 宁波睿达智能装备</em>",
    tb=PRJ_TB, side_f=PRJ_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px">'
        # 项目摘要条
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:84px">'
        '<span class="tilemark">' + ic("layout-kanban", 20) + "</span>"
        '<div style="margin-left:14px">'
        '<div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        "宁波睿达智能装备 · 智能仓储与安防集成项目</div>"
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:4px">'
        "商机 SJ-2609-047 · 合同额 ¥2,680,000 · 负责人 周靖川 · 进入方案沟通已 18 天</div></div>"
        '<div style="margin-left:auto;display:flex;align-items:center;gap:20px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">当前阶段</div>'
        '<div style="margin-top:5px"><span class="tagch" style="border-color:rgba(34,211,238,.5);'
        'background:rgba(34,211,238,.13);color:#67E8F9">方案沟通</span></div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">下一阶段</div>'
        '<div style="margin-top:5px"><span class="tagch" style="border-color:rgba(251,191,36,.5);'
        'background:rgba(251,191,36,.12);color:#FCD34D">商务及采购对应</span></div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">赢单概率</div>'
        "<div style=\"font-size:20px;font-weight:600;font-family:'Geist Mono',monospace;"
        'margin-top:3px">75%</div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">预计签约</div>'
        "<div style=\"font-size:20px;font-weight:600;font-family:'Geist Mono',monospace;"
        'margin-top:3px">10-15</div></div></div></div>'
        # 两栏：阶段流 + 阶段工作台
        '<div class="row" style="grid-template-columns:minmax(0,1.12fr) minmax(0,1fr)">'
        + panel("阶段推进 · 8 个阶段", stage_flow(FLOW, CUR),
                sub="已完成 4 段 · 当前第 5 段 · 剩余 3 段",
                right=chip("推进到下一阶段", "arrow-narrow-right", True))
        + panel("当前阶段工作台", (
            '<div style="padding:14px 16px">'
            '<div style="display:flex;align-items:center;gap:9px;margin-bottom:10px">'
            '<span class="tagch" style="border-color:rgba(34,211,238,.5);background:rgba(34,211,238,.13);'
            'color:#67E8F9">方案沟通</span>'
            '<span style="font-size:11.5px;color:var(--s-t3)">执行点清单 · 4 项</span></div>'
            + timeline([
                ("ok", "方案初稿讲解完成", "09-16 · 客户技术部与使用部门共同参加"),
                ("ok", "客户技术问题清单回收", "09-18 · 共 12 条，已答复 12 条"),
                ("acc", "竞品对比说明材料", "进行中 · 预计 09-24 提交"),
                ("mute", "二次报价与配置调整", "待办 · 依赖竞品信息回收"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:14px 0"></div>'
            '<div style="display:flex;align-items:center;gap:9px;margin-bottom:10px">'
            '<span class="tagch" style="border-color:rgba(34,211,238,.5);background:rgba(34,211,238,.13);'
            'color:#67E8F9">关键点核对</span>'
            '<span style="font-size:11.5px;color:var(--s-t3)">3 项，已达成 1 项</span></div>'
            + timeline([
                ("ok", "技术方案无重大异议", "已确认 · 09-18"),
                ("warn", "摸清竞品报价与评标口径", "待办 · 采购部口径尚未明确"),
                ("mute", "确认使用部门签字人", "待办 · 需与客户项目经理确认"),
            ])
            + '<div style="margin-top:14px;padding:11px 13px;background:rgba(251,191,36,.08);'
            'border:1px solid rgba(251,191,36,.3);border-radius:9px;font-size:11.5px;'
            'color:#FCD34D;line-height:1.65">' + ic("alert-triangle", 13)
            + " 风险提示：客户采购部要求补充 3 年运维报价，需在进入商务阶段前给出，"
            "否则会拖长方案沟通周期。</div></div>"
        ), sub="本阶段做什么 · 达成什么",
            right=chip("下一阶段准备清单", "list-details")),
        "</div>"
        "</div>"
    ),
)
