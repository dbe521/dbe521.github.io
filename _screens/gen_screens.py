# -*- coding: utf-8 -*-
"""gen_screens.py · 14 个系统界面示意图的定义与生成

跑这个脚本会生成 14 个 HTML 到当前目录，再由 render.sh 渲染成图。
改文案/字段/数值只需改这里的 SCREENS。
"""

import os
from gen_lib import (
    ic, esc, tag, kpi, kpis, panel, chip, table, donut, area_chart,
    legend_inline, bar_chart, funnel, map_panel, kv, timeline,
    progress_rows, stat_row, steps_bar, page,
)

from _new01 import S01N, S01BN
from _new02 import S02N, S02BN

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE_TS = "数据更新于 2026-09-21 09:42"


def tb_right(period, name, role, badge="3"):
    return (
        '<div class="tb-pill">%s%s%s</div>'
        '<div class="tb-ic">%s<b>%s</b></div>'
        '<div class="tb-user"><span class="av">%s</span><u>%s · %s</u></div>'
        % (ic("calendar", 13), esc(period), ic("chevron-down", 12),
           ic("bell", 15), badge, esc(name[:2]), esc(name), esc(role))
    )


def mid(left, right, ratio="2.15fr 1fr"):
    return '<div class="row" style="grid-template-columns:%s">%s%s</div>' % (ratio, left, right)


def canvas(*parts):
    """把若干片段按顺序拼成画布内容（允许 3 段标准布局，也允许自定义结构）"""
    return "".join(parts)


# ============================================================ 01 AI 财务超级助理

FIN_NAV = [
    ("经营总览", ""), ("票据识别", ""), ("银企对账", ""), ("单据审核", "28"),
    ("费用政策", ""), ("应收核销", ""), ("应付管理", ""), ("关账看板", ""),
    ("#归档与配置", ""), ("财务档案", ""), ("系统设置", ""),
]
FIN_SIDE_F = '<span>账期 2026-09</span><span class="tag warn">关账进行中</span>'

S01 = dict(
    id="01-ai-finance-overview", name="AI 财务超级助理", en="AI FINANCE COPILOT",
    nav=FIN_NAV, active="经营总览", crumb="财务共享 <em>/ 经营总览</em>",
    tb=tb_right("2026 年 9 月", "李静", "财务负责人"),
    side_f=FIN_SIDE_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="待审单据", value="28", unit="张", tone="warn",
                 desc="其中 <b>5 张</b>已超 3 天未处理"),
            dict(label="自动匹配成功", value="1,486", unit="笔", tone="ok",
                 desc="差异挂账 <b>46 笔</b>待人工确认"),
            dict(label="费用政策自动命中", value="63", unit="笔", tone="acc",
                 desc="自动放行 58 笔 · 转复核 5 笔"),
            dict(label="本月关账进度", value="第 3 步 · 费用归集", tone="acc", steps=(2, 2, 6)),
        ]),
        mid(
            panel("待审单据", table(
                [("单据编号", 16, ""), ("类型", 13, ""), ("金额", 12, "num"),
                 ("申请人", 12, ""), ("部门", 15, ""), ("风险标签", 16, ""), ("状态", 16, "")],
                [
                    ["BX-202609-0431", "差旅报销", "¥3,180.00", "陈嘉铭", "华东销售部", tag("超标提示", "warn"), tag("待复核", "info")],
                    ["BX-202609-0430", "业务招待", "¥1,260.00", "周雨桐", "市场部", tag("缺附件", "warn"), tag("待复核", "info")],
                    ["FP-202609-1187", "增值税专票", "¥8,640.00", "系统识别", "采购部", tag("已验真", "ok"), tag("已入账", "ok")],
                    ["BX-202609-0429", "交通补贴", "¥480.00", "邵天成", "交付一部", tag("无", "mute"), tag("已入账", "ok")],
                    ["BX-202609-0428", "差旅报销", "¥2,050.00", "林思远", "华东销售部", tag("疑似重复", "bad"), tag("已拦截", "bad")],
                    ["FP-202609-1186", "增值税普票", "¥1,920.00", "系统识别", "财务共享", tag("已验真", "ok"), tag("已入账", "ok")],
                    ["BX-202609-0427", "办公用品", "¥736.00", "赵敏行", "综合管理部", tag("无", "mute"), tag("已入账", "ok")],
                    ["BX-202609-0425", "培训费", "¥2,880.00", "孙亦雯", "人力资源部", tag("超预算", "bad"), tag("待复核", "info")],
                ]),
                sub="按风险等级排序",
                right=chip("筛选", "filter") + chip("导出", "download")),
            panel("本月费用分布", donut(
                [("#22D3EE", 28.4, "采购付款", "342,800"),
                 ("#60A5FA", 52.2, "差旅报销", "186,400"),
                 ("#FBBF24", 8.9, "业务招待", "58,200"),
                 ("#34D399", 6.3, "办公费用", "41,600"),
                 ("#5A616E", 4.2, "其他", "27,900")],
                "¥65.7万", "本月累计"), sub="按科目归集"),
        ),
        panel("近 30 日单据处理量", area_chart(
            [("#FBBF24", 1.6, [96, 128, 112, 146, 130, 158, 142, 172, 154, 186, 168], 0.26, "251,191,36"),
             ("#22D3EE", 1.8, [1180, 1140, 1210, 1170, 1230, 1190, 1250, 1215, 1270, 1235, 1258], 0.18, "34,211,238")],
            ["1,800", "1,200", "600", "0"],
            [(44, "08-23", "start"), (271, "08-29", "middle"), (498, "09-05", "middle"),
             (726, "09-12", "middle"), (953, "09-18", "middle"), (1180, "09-21", "end")],
            vmax=1500),
            sub="自动处理与人工复核",
            right=legend_inline([("#22D3EE", "自动处理 13,526 笔"), ("#FBBF24", "人工复核 1,693 笔")])),
    ),
)

# ======================================================== 01b AI 财务 · 单据详情

S01B = dict(
    id="01b-ai-finance-detail", name="AI 财务超级助理", en="AI FINANCE COPILOT",
    nav=FIN_NAV, active="单据审核", crumb="单据审核 <em>/ BX-202609-0431</em>",
    tb=tb_right("2026 年 9 月", "李静", "财务负责人", "5"),
    side_f=FIN_SIDE_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px;min-height:0">'
        # 顶部单据摘要
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<div style="display:flex;align-items:center;gap:14px">'
        '<span class="tilemark">' + ic("file-invoice", 20) + "</span>"
        '<div><div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        'BX-202609-0431 · 差旅报销</div>'
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        '陈嘉铭 · 华东销售部 · 提交于 2026-09-20 18:24</div></div></div>'
        '<div style="margin-left:auto;display:flex;align-items:center;gap:22px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">申请金额</div>'
        '<div style="font-size:20px;font-weight:600;letter-spacing:-.02em;font-family:\'Geist Mono\',monospace">¥3,180.00</div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">系统初审</div>'
        '<div style="margin-top:5px">' + tag("超标提示", "warn") + "</div></div>"
        '<span class="chip acc">' + ic("user-check", 13) + "人工复核</span>"
        '<span class="chip">' + ic("check", 13) + "确认入账</span>"
        "</div></div>"
        # 三栏主体
        '<div class="row" style="grid-template-columns:320px minmax(0,1fr) 340px">'
        # 票据影像
        + panel("票据影像", (
            '<div style="padding:14px">'
            '<div class="receipt">'
            '<div class="rc-hd">增值税电子普通发票</div>'
            '<div class="rc-no">发票号码 04288196</div>'
            '<div class="rc-l"></div><div class="rc-l" style="width:82%"></div>'
            '<div class="rc-l" style="width:66%"></div><div class="rc-l" style="width:74%"></div>'
            '<div class="rc-amt">¥ 3,180.00</div>'
            '<div class="rc-l" style="width:58%"></div>'
            '<div class="rc-seal">已验真</div>'
            "</div>"
            '<div style="display:flex;align-items:center;gap:8px;margin-top:12px;font-size:11.5px;color:var(--s-t3)">'
            + ic("scan", 14) + "共 2 张 · 识别置信度 98.6%</div>"
            '<div style="display:flex;gap:8px;margin-top:12px">'
            + chip("上一张") + chip("下一张") + "</div>"
            "</div>"
        ), sub="OCR 识别结果"),
        # 结构化字段
        panel("结构化字段与校验结果", (
            '<div class="row" style="grid-template-columns:1fr 1fr;gap:0">'
            + kv([
                ("发票代码", "<b>011002000</b>"), ("发票号码", "<b>04288196</b>"),
                ("开票日期", "<b>2026-09-18</b>"), ("销方名称", "<b>杭州云栈酒店管理</b>"),
                ("价税合计", "<b>¥3,180.00</b>"), ("税额", "<b>¥180.00</b>"),
                ("查验状态", tag("已验真", "ok")), ("查重结果", tag("无重复", "mute")),
            ])
            + kv([
                ("报销类别", "<b>差旅住宿</b>"), ("出差事由", "<b>华东区客户现场支持</b>"),
                ("入住天数", "<b>3 晚</b>"), ("人均标准", "<b>¥600 / 晚</b>"),
                ("实际单价", "<b>¥1,060 / 晚</b>"), ("超标金额", "<b style='color:#FCD34D'>¥1,380.00</b>"),
                ("政策依据", "<b>差旅费管理办法 第 12 条</b>"), ("审批链", "<b>部门负责人 → 财务</b>"),
            ])
            + "</div>"
        ), sub="共 16 个字段 · 2 项需人工确认"),
        # 处理留痕
        panel("处理留痕", timeline([
            ("ok", "提交报销单", "陈嘉铭 · 09-20 18:24"),
            ("ok", "OCR 识别完成", "识别 2 张票据，字段 16 项 · 09-20 18:24"),
            ("ok", "发票查验通过", "税务平台返回一致 · 09-20 18:25"),
            ("acc", "规则校验命中", "差旅费管理办法 第 12 条：住宿超标 ¥1,380.00 · 09-20 18:25"),
            ("mute", "转人工复核", "待财务确认超标事由 · 处理人：李静"),
        ]), sub="全链路可回溯", right=chip("导出留痕", "download")),
        "</div>"
        "</div>"
    ),
)

# ==================================================== 02 AI 项目成交推进系统

PRJ_NAV = [
    ("经营总览", ""), ("商机管理", "12"), ("客户档案", ""), ("方案报价", ""),
    ("合同管理", ""), ("交付计划", ""), ("变更单", "3"), ("验收与回款", ""),
    ("#资源", ""), ("资源排期", ""),
]
PRJ_F = '<span>本季度目标 4,200 万</span><span class="tag ok">已完成 68%</span>'

S02 = dict(
    id="02-project-overview", name="AI 项目成交推进系统", en="PROJECT DEAL PIPELINE",
    nav=PRJ_NAV, active="经营总览", crumb="经营总览",
    tb=tb_right("2026 年 9 月", "周靖川", "销售总监"),
    side_f=PRJ_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="在跟商机", value="47", unit="个", tone="acc", desc="已立项 <b>12 个</b> · 报价中 9 个"),
            dict(label="本月新签", value="1,860", unit="万", tone="ok", desc="较上月 <i>+5 个项目</i>"),
            dict(label="里程碑超期", value="3", unit="项", tone="warn", desc="其中 <b>1 项</b>已影晌交付"),
            dict(label="待回款", value="1,240", unit="万", tone="bad", desc="逾期 <b>180 万</b> · 涉及 4 个客户"),
        ]),
        mid(
            panel("项目台账", table(
                [("项目编号", 15, ""), ("客户", 22, ""), ("当前阶段", 14, ""),
                 ("合同额", 12, "num"), ("交付进度", 14, ""), ("负责人", 11, ""), ("健康度", 12, "")],
                [
                    ["PJ-2609-018", "宁波睿达智能装备", "方案报价", "268,000", "18%", "周靖川", tag("正常", "ok")],
                    ["PJ-2609-014", "苏州工业园区管委会", "技术对接", "1,960,000", "12%", "吴桐", tag("正常", "ok")],
                    ["PJ-2608-231", "杭州海联电子", "交付实施", "486,000", "62%", "陆铭", tag("预警", "warn")],
                    ["PJ-2608-219", "无锡恒信精密", "验收回款", "328,000", "92%", "周靖川", tag("正常", "ok")],
                    ["PJ-2607-164", "合肥创元新材料", "交付实施", "742,000", "54%", "陆铭", tag("超期", "bad")],
                    ["PJ-2607-152", "嘉兴瑞光电工", "验收回款", "156,000", "88%", "吴桐", tag("正常", "ok")],
                    ["PJ-2606-098", "绍兴越信纺织", "交付实施", "520,000", "76%", "陆铭", tag("正常", "ok")],
                    ["PJ-2606-071", "义乌新亚商贸", "质保期", "98,000", "100%", "吴桐", tag("已结项", "mute")],
                ]),
                sub="按健康度与合同额排序",
                right=chip("筛选", "filter") + chip("导出", "download")),
            panel("成交阶段分布", funnel([
                ("线索", "192"), ("商机", "47"), ("报价", "21"), ("签约", "9"), ("交付中", "6"),
            ]), sub="近 90 天"),
        ),
        panel("回款计划与实际", bar_chart(
            ["4月", "5月", "6月", "7月", "8月", "9月"],
            [386, 342, 448, 401, 268, 196],
            ["500", "375", "250", "125", "0"], vmax=500,
            values2=[420, 386, 512, 468, 296, 340], color2="#FBBF24"),
            sub="单位：万元",
            right=legend_inline([("#FBBF24", "计划回款 2,422 万"), ("#22D3EE", "实际回款 2,041 万")])
            + chip("查看明细")),
    ),
)

# ==================================================== 02b 项目详情

S02B = dict(
    id="02b-project-detail", name="AI 项目成交推进系统", en="PROJECT DEAL PIPELINE",
    nav=PRJ_NAV, active="交付计划", crumb="交付计划 <em>/ PJ-2608-231</em>",
    tb=tb_right("2026 年 9 月", "周靖川", "销售总监"),
    side_f=PRJ_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto auto minmax(0,1fr);gap:16px;min-height:0">'
        # 项目头
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<div><div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        'PJ-2608-231 · 杭州海联电子智能仓储项目</div>'
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        '合同额 ¥486,000 · 签约 2026-08-14 · 交付负责人 陆铭</div></div>'
        '<div style="margin-left:auto;display:flex;align-items:center;gap:20px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">交付进度</div>'
        '<div style="font-size:20px;font-weight:600;font-family:\'Geist Mono\',monospace">62%</div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">项目健康度</div>'
        '<div style="margin-top:5px">' + tag("预警", "warn") + "</div></div>"
        '<span class="chip acc">' + ic("list-details", 13) + "变更单 2 张</span></div></div>"
        # 阶段推进
        + panel("阶段推进", (
            '<div style="display:flex;align-items:center;padding:18px 20px">'
            + "".join(
                '<div style="flex:1;text-align:center">'
                '<div style="height:6px;border-radius:3px;background:%s;margin-bottom:10px"></div>'
                '<div style="font-size:12.5px;color:%s;font-weight:%s">%s</div>'
                '<div style="font-size:11px;color:var(--s-t3);margin-top:3px">%s</div></div>'
                % (c, tc, w, n, d)
                for c, tc, w, n, d in [
                    ("#34D399", "#EDF1F7", "400", "技术对接", "已完成 · 08-22"),
                    ("#34D399", "#EDF1F7", "400", "方案确认", "已完成 · 09-01"),
                    ("#22D3EE", "#EDF1F7", "500", "设备进场", "进行中 · 计划 09-25"),
                    ("#1C212A", "#737B8B", "400", "安装调试", "计划 10-08"),
                    ("#1C212A", "#737B8B", "400", "验收交付", "计划 10-20"),
                ]
            )
            + "</div>"
        ), sub="共 5 个阶段"),
        # 里程碑 + 成本 + 回款
        '<div class="row" style="grid-template-columns:minmax(0,1.15fr) 340px">'
        + panel("里程碑计划", table(
            [("里程碑", 34, ""), ("计划日期", 18, ""), ("实际/预计", 18, ""), ("责任人", 14, ""), ("状态", 16, "")],
            [
                ["设备清单确认", "2026-09-05", "2026-09-05", "陆铭", tag("已完成", "ok")],
                ["首批设备到场", "2026-09-18", "2026-09-22", "陆铭", tag("延期 4 天", "warn")],
                ["安装完成", "2026-10-08", "2026-10-08", "冯昊", tag("按计划", "info")],
                ["系统联调", "2026-10-15", "2026-10-15", "冯昊", tag("按计划", "info")],
                ["客户验收", "2026-10-20", "2026-10-20", "周靖川", tag("按计划", "info")],
            ]), sub="1 项延期", right=chip("催办")),
        panel("成本归集与回款", (
            progress_rows([
                ("设备采购", 82, "¥246,000 / ¥300,000"),
                ("人工与服务", 46, "¥38,000 / ¥82,000"),
                ("差旅与外协", 68, "¥21,000 / ¥31,000"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:0 16px"></div>'
            + stat_row([("已回款", "292,000", ""), ("待回款", "194,000", "")])
            + '<div style="padding:0 16px 14px;font-size:11.5px;color:var(--s-t3)">'
            + "两笔待回款对应第二、三次验收节点</div>"
        ), sub="预算 ¥486,000"),
        "</div>",
        "</div>"
    ),
)

# ================================================== 03 AI 企业经营决策中心

BIZ_NAV = [
    ("经营驾驶舱", ""), ("指标字典", ""), ("异动归因", "5"), ("经营例会", ""),
    ("待办中心", "9"), ("数据源管理", ""), ("权限与审计", ""),
]
BIZ_F = '<span>指标口径版本 v1.4</span><span class="tag ok">已校验</span>'

S03 = dict(
    id="03-biz-cockpit", name="AI 企业经营决策中心", en="BUSINESS DECISION CENTER",
    nav=BIZ_NAV, active="经营驾驶舱", crumb="经营驾驶舱 <em>/ 集团总览</em>",
    tb=tb_right("2026 年 9 月", "沈立言", "总经理", "5"),
    side_f=BIZ_F, note=NOTE_TS,
    canvas=(
        # 4 个核心经营数
        '<div class="kpis">'
        '<div class="kpi acc"><div class="kpi-k">营业收入（本月累计）</div>'
        '<div class="kpi-v">4,286<u>万</u></div>'
        '<div class="kpi-d">达成率 91% · 落后时间进度 <b>4 天</b></div></div>'
        '<div class="kpi warn"><div class="kpi-k">主营业务毛利</div>'
        '<div class="kpi-v">936<u>万</u></div>'
        '<div class="kpi-d">较上月下降 <b>62 万</b> · 点击查看归因</div></div>'
        '<div class="kpi ok"><div class="kpi-k">经营性现金净流入</div>'
        '<div class="kpi-v">418<u>万</u></div>'
        '<div class="kpi-d">连续 3 个月为正</div></div>'
        '<div class="kpi ok"><div class="kpi-k">客户续约与满意度</div>'
        '<div class="kpi-v">4.6<u>分</u></div>'
        '<div class="kpi-d">续约 21 家 · 流失预警 <b>2 家</b></div></div>'
        "</div>"
        + mid(
            panel("经营指标趋势", area_chart(
                [("#22D3EE", 1.6, [362, 388, 410, 396, 442, 468, 451, 486, 472, 508, 496], 0.2, "34,211,238")],
                ["600", "450", "300", "150", "0"],
                [(44, "08-23", "start"), (271, "08-29", "middle"), (498, "09-05", "middle"),
                 (726, "09-12", "middle"), (953, "09-18", "middle"), (1180, "09-21", "end")],
                vmax=600),
                sub="营业收入·日累计（万元）",
                right=legend_inline([("#22D3EE", "本月 4,286 万")]) + chip("切换指标", "chevron-down")),
            panel("异动归因", (
                '<div style="padding:14px 16px">'
                '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:12px">'
                '毛利下降 62 万的主要来源</div>'
                + progress_rows([
                    ("硬件采购成本上升", 78, "−38.6 万"),
                    ("华东区折扣加深", 41, "−20.4 万"),
                    ("服务人工成本", 8, "−3.0 万"),
                ])
                + '<div style="border-top:1px solid var(--s-line);margin:4px 0 10px"></div>'
                '<div style="font-size:11.5px;color:var(--s-t3);line-height:1.6">'
                "结论可下钻至原始采购单与销售合同，共 26 条单据</div>"
                '<div style="margin-top:12px">' + chip("下钻查看", "arrow-right", True) + "</div>"
                "</div>"
            ), sub="自动拆解"),
        ),
        panel("数据源与用数入口", (
            '<div style="display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:18px;padding:14px 18px">'
            '<div class="timeline">'
            + "".join(
                '<div class="tl"><span class="tl-i %s"></span><div style="flex:1">'
                '<div class="tl-t">%s</div><div class="tl-d">%s</div></div>'
                '<span style="font-size:11px;color:var(--s-t3);font-family:\'Geist Mono\',monospace">%s</span></div>'
                % i for i in [
                    ("acc", "华东区毛利下滑 4.2 个百分点", "已定位到 3 个客户合同的折扣条款变动", "09:12"),
                    ("warn", "存货周转天数升至 68 天", "主要集中在智能硬件品类", "08:40"),
                    ("ok", "现金流连续 3 月为正", "应收账款回收加快 6 天", "08:05"),
                    ("mute", "华南区续约率低于目标", "本月 2 家客户未续约", "07:50"),
                ]
            )
            + "</div>"
            '<div style="background:var(--s-panel-2);border:1px solid var(--s-line);'
            'border-radius:10px;padding:14px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:9px">'
            + ic("message", 14) + " 直接提问</div>"
            '<div style="background:var(--s-bg);border:1px solid var(--s-line);border-radius:8px;'
            'padding:11px 12px;font-size:12.5px;color:var(--s-t1);line-height:1.55">'
            "华东区这月毛利率为什么掉了？</div>"
            '<div style="margin-top:10px;font-size:11.5px;color:var(--s-t3);line-height:1.6">'
            "回答引用统一指标口径，结论可下钻到原始单据</div>"
            '<div style="margin-top:12px;display:flex;gap:8px">'
            + chip("华东区 · 毛利率", None, True) + chip("存货周转") + "</div>"
            "</div></div>"
        ), sub="数据更新至今日 09:42", right=chip("3 个数据源正常", "database")),
    ),
)

# ================================================== 03b 指标下钻

S03B = dict(
    id="03b-metric-drill", name="AI 企业经营决策中心", en="BUSINESS DECISION CENTER",
    nav=BIZ_NAV, active="异动归因", crumb="异动归因 <em>/ 华东区毛利率</em>",
    tb=tb_right("2026 年 9 月", "沈立言", "总经理", "5"),
    side_f=BIZ_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px;min-height:0">'
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<div><div class="mono" style="color:var(--s-acc);font-size:11px">DRILL DOWN</div>'
        '<div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em;margin-top:5px">'
        '华东区 · 主营业务毛利率</div></div>'
        '<div style="margin-left:auto;display:flex;align-items:center;gap:22px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">本期</div>'
        '<div style="font-size:20px;font-weight:600;font-family:\'Geist Mono\',monospace">21.4%</div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">同比</div>'
        '<div style="font-size:20px;font-weight:600;color:#FCA5A5;font-family:\'Geist Mono\',monospace">−4.2pp</div></div>'
        '<span class="chip acc">' + ic("history", 13) + "查看口径版本</span></div></div>"
        + '<div class="row" style="grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)">'
        + panel("下钻路径", table(
            [("层级", 18, ""), ("对象", 34, ""), ("本期", 14, "num"), ("同比变化", 18, "num"), ("操作", 16, "")],
            [
                ["集团", "主营业务毛利率", "26.8%", "+0.4pp", chip("已展开")],
                ["区域", "<b>华东区</b>", "21.4%", "−4.2pp", chip("已展开", None, True)],
                ["客户", "宁波睿达智能装备", "18.2%", "−6.8pp", chip("下钻", "arrow-right")],
                ["客户", "杭州海联电子", "22.6%", "−1.9pp", chip("下钻", "arrow-right")],
                ["合同", "PJ-2608-231 硬件折扣条款", "16.4%", "−8.1pp", chip("下钻", "arrow-right")],
                ["成本项", "视频监控设备采购单价", "—", "+7.3%", chip("下钻", "arrow-right")],
            ]), sub="从汇总数到原始单据共 3 层", right=chip("导出路径")),
        panel("归因构成", (
            '<div style="padding:14px 16px">'
            + progress_rows([
                ("硬件采购单价上涨", 62, "−2.6pp"),
                ("销售折扣加深", 33, "−1.4pp"),
                ("服务人工成本上升", 5, "−0.2pp"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:6px 0 12px"></div>'
            '<div style="font-size:12.5px;color:var(--s-t2);line-height:1.7">'
            "<b>建议</b>：宁波睿达合同硬件折扣已达 18%，建议在下次续约时"
            "将服务包与硬件分开报价。</div>"
            '<div style="margin-top:14px;display:flex;gap:8px">'
            + chip("派发待办", "arrow-right", True) + chip("生成例会材料") + "</div></div>"
        ), sub="按贡献度排序"),
        "</div>",
        "</div>"
    ),
)

# ==================================================== 04 智能打印管控

PRT_NAV = [
    ("打印概览", ""), ("用户与权限", ""), ("设备管理", ""), ("配额策略", ""),
    ("留底检索", "6"), ("敏感规则", ""), ("水印规则", ""), ("成本报表", ""),
    ("#运维", ""), ("设备状态", ""),
]
PRT_F = '<span>策略版本 2026-09-18</span><span class="tag ok">已下发 32 台</span>'

S04 = dict(
    id="04-print-control", name="智能打印管控", en="PRINT GOVERNANCE",
    nav=PRT_NAV, active="打印概览", crumb="打印概览 <em>/ 总部办公区</em>",
    tb=tb_right("2026 年 9 月", "何砚清", "行政与 IT 负责人", "6"),
    side_f=PRT_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="今日打印任务", value="1,284", unit="件", tone="acc", desc="已释放 1,196 件 · 未取件 88 件"),
            dict(label="认证释放", value="1,196", unit="件", tone="ok", desc="刷卡 986 · 扫码 210"),
            dict(label="敏感件拦截", value="6", unit="件", tone="bad", desc="转审批 <b>4 件</b> · 已放行 2 件"),
            dict(label="本月纸张用量", value="42,860", unit="张", tone="warn", desc="较配额余 <b>7,140 张</b>"),
        ]),
        mid(
            panel("打印留底记录", table(
                [("时间", 12, ""), ("操作人", 11, ""), ("文档名", 26, ""), ("页数", 8, "num"),
                 ("密级", 12, ""), ("水印", 11, ""), ("状态", 12, "")],
                [
                    ["09-21 09:38", "陈嘉铭", "华东区客户报价单_v3.pdf", "12", tag("秘密", "bad"), tag("已加", "ok"), tag("已释放", "ok")],
                    ["09-21 09:31", "周雨桐", "2026 秋季市场方案.pptx", "28", tag("内部", "info"), tag("已加", "ok"), tag("已释放", "ok")],
                    ["09-21 09:24", "李静", "9月费用报销汇总.xlsx", "6", tag("内部", "info"), tag("已加", "ok"), tag("已释放", "ok")],
                    ["09-21 09:12", "陆铭", "海联电子验收清单.docx", "9", tag("内部", "info"), tag("已加", "ok"), tag("待取件", "warn")],
                    ["09-21 08:58", "吴桐", "设备采购合同（终版）.pdf", "22", tag("机密", "bad"), tag("已加", "ok"), tag("转审批", "warn")],
                    ["09-21 08:46", "冯昊", "机房布线图_A3.pdf", "3", tag("内部", "info"), tag("已加", "ok"), tag("已释放", "ok")],
                    ["09-21 08:31", "邵天成", "员工手册2026.pdf", "46", tag("公开", "mute"), tag("不加", "mute"), tag("已释放", "ok")],
                    ["09-21 08:20", "陈嘉铭", "投标文件（涉密）.pdf", "86", tag("机密", "bad"), tag("已加", "ok"), tag("已拦截", "bad")],
                ]),
                sub="全文可检索",
                right=chip("按关键字检索", "search") + chip("导出审计", "download")),
            panel("部门印量（本月）", bar_chart(
                ["销售", "交付", "财务", "市场", "行政", "研发"],
                [9860, 8240, 6180, 5260, 3980, 2860],
                ["10,000", "7,500", "5,000", "2,500", "0"], vmax=10000),
                sub="单位：张", right=legend_inline([("#22D3EE", "彩色 18%")])),
        ),
        panel("设备状态与耗材余量", (
            '<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;padding:16px 18px">'
            + "".join(
                '<div style="background:var(--s-panel-2);border:1px solid var(--s-line);border-radius:10px;padding:12px">'
                '<div style="display:flex;align-items:center;justify-content:space-between">'
                '<span style="font-size:12.5px;font-weight:500">%s 层 %s</span>%s</div>'
                '<div style="font-size:11px;color:var(--s-t3);margin:7px 0 9px">%s · 本月 %s 张</div>'
                '<div style="font-size:11px;color:var(--s-t3);margin-bottom:5px">碳粉余量</div>'
                '<div class="bar"><i style="width:%s%%;background:%s"></i></div></div>'
                % d for d in [
                    ("3", "A 区", tag("在线", "ok"), "MFP-C5580", "9,860", 72, "#34D399"),
                    ("3", "B 区", tag("在线", "ok"), "MFP-C5580", "8,240", 46, "#FBBF24"),
                    ("5", "前台", tag("在线", "ok"), "MFP-C3570", "6,180", 88, "#34D399"),
                    ("8", "财务", tag("缺纸", "warn"), "MFP-C3570", "4,120", 22, "#F87171"),
                    ("12", "研发", tag("在线", "ok"), "MFP-B4540", "2,860", 64, "#34D399"),
                    ("18", "仓库", tag("离线", "bad"), "MFP-B4540", "1,604", 12, "#F87171"),
                ]
            )
            + "</div>"
        ), sub="共 32 台 · 2 台需处理", right=chip("一键催耗材", "refresh")),
    ),
)

# ==================================================== 04b 留底检索与敏感件审批

S04B = dict(
    id="04b-print-archive", name="智能打印管控", en="PRINT GOVERNANCE",
    nav=PRT_NAV, active="留底检索", crumb="留底检索 <em>/ 审计台账</em>",
    tb=tb_right("2026 年 9 月", "何砚清", "行政与 IT 负责人", "6"),
    side_f=PRT_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px;min-height:0">'
        # 检索条
        '<div class="panel" style="flex-direction:row;align-items:center;gap:12px;padding:0 18px;height:76px">'
        '<span class="chip acc">' + ic("search", 13) + "关键字：合同" + "</span>"
        '<span class="chip">' + ic("calendar", 13) + "近 30 天</span>"
        '<span class="chip">' + ic("user", 13) + "全部人员</span>"
        '<span class="chip">' + ic("fingerprint", 13) + "密级：机密 / 秘密" + "</span>"
        '<div style="margin-left:auto;display:flex;align-items:center;gap:12px">'
        '<span style="font-size:12.5px;color:var(--s-t3)">命中 36 条 · 已标红 6 条</span>'
        + chip("导出审计报告", "download", True) + "</div></div>"
        + '<div class="row" style="grid-template-columns:minmax(0,1.6fr) minmax(0,1fr)">'
        + panel("检索结果", table(
            [("时间", 13, ""), ("操作人", 11, ""), ("文档名", 30, ""), ("页数", 7, "num"),
             ("密级", 11, ""), ("命中规则", 16, ""), ("状态", 12, "")],
            [
                ["09-21 08:20", "陈嘉铭", "投标文件（涉密）.pdf", "86", tag("机密", "bad"), "涉密关键字", tag("已拦截", "bad")],
                ["09-21 08:58", "吴桐", "设备采购合同（终版）.pdf", "22", tag("机密", "bad"), "合同类文件", tag("转审批", "warn")],
                ["09-20 17:42", "陆铭", "海联电子维保合同.pdf", "14", tag("秘密", "bad"), "合同类文件", tag("已放行", "ok")],
                ["09-20 16:08", "周靖川", "宁波睿达框架协议.docx", "18", tag("秘密", "bad"), "合同类文件", tag("已放行", "ok")],
                ["09-20 14:36", "李静", "年度审计合同附件.pdf", "32", tag("内部", "info"), "合同类文件", tag("已放行", "ok")],
                ["09-19 11:20", "冯昊", "施工分包合同.pdf", "12", tag("内部", "info"), "合同类文件", tag("已放行", "ok")],
                ["09-19 09:54", "邵天成", "供应商保密协议.pdf", "6", tag("秘密", "bad"), "保密类关键字", tag("已放行", "ok")],
                ["09-18 15:12", "赵敏行", "租赁合同续签.pdf", "8", tag("内部", "info"), "合同类文件", tag("已放行", "ok")],
            ]), sub="按命中规则与时间排序"),
        panel("敏感件审批", (
            '<div style="padding:16px">'
            '<div style="background:var(--s-panel-2);border:1px solid var(--s-line-2);border-radius:10px;padding:14px">'
            '<div style="display:flex;align-items:center;justify-content:space-between">'
            '<span style="font-size:13px;font-weight:500">投标文件（涉密）.pdf</span>'
            + tag("机密", "bad") + "</div>"
            '<div style="font-size:11.5px;color:var(--s-t3);margin:8px 0 12px">'
            "陈嘉铭 · 华东销售部 · 86 页 · 命中「投标 / 报价 / 涉密」</div>"
            + kv([("水印策略", "<b>强制姓名 + 部门 + 时间</b>"), ("二维码追溯", "<b>已启用</b>"),
                  ("审批人", "<b>何砚清 → 沈立言</b>"), ("当前状态", tag("待一级审批", "warn"))])
            + '<div style="display:flex;gap:8px;margin-top:14px">'
            + chip("批准放行", "check", True) + chip("驳回") + "</div></div>"
            '<div style="margin-top:16px;font-size:12.5px;color:var(--s-t2);margin-bottom:10px">'
            "近 30 天敏感件拦截趋势</div>"
            + area_chart(
                [("#F87171", 1.6, [2, 4, 3, 6, 5, 8, 6, 9, 7, 6, 6], 0.22, "248,113,113")],
                ["9", "6", "3", "0"],
                [(44, "08-23", "start"), (498, "09-05", "middle"), (953, "09-18", "middle"), (1180, "09-21", "end")],
                vmax=9, height=110, top=8)
            + "</div>"
        ), sub="待审批 2 件"),
        "</div>",
        "</div>"
    ),
)

# ================================================== 05 智能抄表及账单系统

MTR_NAV = [
    ("抄表总览", ""), ("设备台账", ""), ("抄表管理", "4"), ("计费规则", ""),
    ("账单管理", ""), ("收缴跟踪", ""), ("异常预警", "7"), ("对账中心", ""),
    ("#客户", ""), ("客户与合同", ""),
]
MTR_F = '<span>本周期 2026-09</span><span class="tag warn">出账中</span>'

S05 = dict(
    id="05-meter-billing", name="智能抄表及账单系统", en="METERING & BILLING",
    nav=MTR_NAV, active="抄表总览", crumb="抄表总览 <em>/ 2026-09 周期</em>",
    tb=tb_right("2026 年 9 月", "顾云卿", "运营主管", "7"),
    side_f=MTR_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="在线设备", value="1,248", unit="台", tone="ok", desc="离线 <b>6 台</b> · 待派单处理"),
            dict(label="本周期采集印量", value="386.4", unit="万页", tone="acc", desc="黑白 342.6 万 · 彩色 43.8 万"),
            dict(label="待出账客户", value="42", unit="户", tone="warn", desc="已核对 386 户 · 差异 <b>4 户</b>"),
            dict(label="读数异常", value="7", unit="户", tone="bad", desc="印量突变 <b>5 户</b> · 未回传 2 户"),
        ]),
        mid(
            panel("客户抄表台账", table(
                [("客户", 22, ""), ("机型", 15, ""), ("上期读数", 12, "num"), ("本期读数", 12, "num"),
                 ("本期印量", 12, "num"), ("抄表方式", 12, ""), ("状态", 15, "")],
                [
                    ["宁波睿达智能装备", "MFP-C5580", "1,286,400", "1,412,860", "126,460", "物联网自动", tag("已采集", "ok")],
                    ["苏州工业园区管委会", "MFP-C6580", "2,640,180", "2,798,420", "158,240", "物联网自动", tag("已采集", "ok")],
                    ["杭州海联电子", "MFP-C3570", "846,200", "918,640", "72,440", "物联网自动", tag("已采集", "ok")],
                    ["无锡恒信精密", "MFP-B4540", "426,800", "468,120", "41,320", "网关采集", tag("已采集", "ok")],
                    ["合肥创元新材料", "MFP-C3570", "618,400", "742,980", "124,580", "网关采集", tag("印量突变", "warn")],
                    ["嘉兴瑞光电工", "MFP-B4540", "312,600", "338,400", "25,800", "人工抄表", tag("待复核", "info")],
                    ["绍兴越信纺织", "MFP-C3570", "586,200", "0", "—", "未回传", tag("设备离线", "bad")],
                    ["义乌新亚商贸", "MFP-C3570", "438,900", "472,360", "33,460", "物联网自动", tag("已采集", "ok")],
                ]),
                sub="按状态排序",
                right=chip("批量抄表", "refresh") + chip("导出台账", "download")),
            panel("机型印量分布", donut(
                [("#22D3EE", 38.6, "MFP-C6580", "149.2 万"),
                 ("#60A5FA", 26.4, "MFP-C5580", "102.0 万"),
                 ("#FBBF24", 19.8, "MFP-C3570", "76.5 万"),
                 ("#34D399", 15.2, "MFP-B4540", "58.7 万")],
                "386.4万", "本周期采集"), sub="共 4 个机型"),
        ),
        panel("近 30 日印量趋势", area_chart(
            [("#FBBF24", 1.6, [9.8, 11.2, 10.4, 12.6, 11.8, 9.2, 13.4, 12.2, 10.6, 13.8, 14.2], 0.24, "251,191,36"),
             ("#22D3EE", 1.8, [82, 88, 84, 96, 90, 78, 102, 94, 86, 104, 108], 0.18, "34,211,238")],
            ["120", "80", "40", "0"],
            [(44, "08-23", "start"), (271, "08-29", "middle"), (498, "09-05", "middle"),
             (726, "09-12", "middle"), (953, "09-18", "middle"), (1180, "09-21", "end")],
            vmax=120),
            sub="单位：万页",
            right=legend_inline([("#22D3EE", "黑白 342.6 万"), ("#FBBF24", "彩色 43.8 万")])
            + chip("异常点标注", "alert-triangle")),
    ),
)

# ================================================== 05b 客户账单明细

S05B = dict(
    id="05b-billing-detail", name="智能抄表及账单系统", en="METERING & BILLING",
    nav=MTR_NAV, active="账单管理", crumb="账单管理 <em>/ BL-202609-0386</em>",
    tb=tb_right("2026 年 9 月", "顾云卿", "运营主管", "7"),
    side_f=MTR_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px;min-height:0">'
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<div><div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        'BL-202609-0386 · 宁波睿达智能装备</div>'
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        '计费周期 2026-09-01 至 2026-09-30 · 机型 MFP-C5580 · 合同 RT-2025-0168</div></div>'
        '<div style="margin-left:auto;display:flex;align-items:center;gap:22px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">本期应付</div>'
        '<div style="font-size:20px;font-weight:600;font-family:\'Geist Mono\',monospace">¥4,286.40</div></div>'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">账单状态</div>'
        '<div style="margin-top:5px">' + tag("已推送待缴", "warn") + "</div></div>"
        '<span class="chip acc">' + ic("arrow-narrow-right", 13) + "推送客户</span>"
        '<span class="chip">' + ic("download", 13) + "下载 PDF" + "</span></div></div>"
        + '<div class="row" style="grid-template-columns:minmax(0,1.55fr) minmax(0,1fr)">'
        + panel("阶梯计价过程", table(
            [("计费项目", 22, ""), ("区间", 28, ""), ("单价", 14, "num"), ("用量", 16, "num"), ("小计", 20, "num")],
            [
                ["黑白印量 · 基础", "0 - 100,000 页", "¥0.0280", "100,000", "¥2,800.00"],
                ["黑白印量 · 超出", "100,001 页以上", "¥0.0230", "26,460", "¥608.58"],
                ["彩色印量 · 基础", "0 - 20,000 页", "¥0.1500", "12,480", "¥1,872.00"],
                ["<b>合计</b>", "—", "—", "<b>138,940 页</b>", "<b>¥5,280.58</b>"],
                ["年度返利抵扣", "合同条款 4.2", "−¥0.0072", "138,940", "−¥994.18"],
                ["<b>本期应付</b>", "—", "—", "—", "<b>¥4,286.40</b>"],
            ]), sub="规则版本 2026-07-01", right=chip("查看规则", "chevron-right")),
        panel("读数来源与追溯", (
            kv([
                ("上期读数", "<b>1,286,400</b>"),
                ("本期读数", "<b>1,412,860</b>"),
                ("本期印量", "<b>126,460 页</b>"),
                ("抄表方式", tag("物联网自动采集", "ok")),
                ("采集时间", "<b>2026-09-30 23:55</b>"),
                ("网关编号", "<b>GW-EA-0217</b>"),
                ("数据校验", tag("两次采集一致", "ok")),
                ("计费依据", "<b>合同 RT-2025-0168</b>"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:2px 16px 0"></div>'
            + '<div style="padding:14px 16px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:10px">推送与收缴记录</div>'
            + timeline([
                ("ok", "账单生成", "09-30 23:58 系统按规则自动出账"),
                ("ok", "推送客户", "10-01 08:02 邮件 + 短信"),
                ("mute", "等待缴费", "客户账期 30 天 · 未逾期"),
            ])
            + "</div>"
        ), sub="每笔可回溯到原始读数"),
        "</div>",
        "</div>"
    ),
)

# ================================================== 06 智能售后服务管理

SVC_NAV = [
    ("服务总览", ""), ("工单池", "14"), ("智能派单", ""), ("工程师地图", ""),
    ("移动作业", ""), ("设备档案", ""), ("备件管理", "3"), ("知识库", ""),
    ("#分析", ""), ("服务分析", ""),
]
SVC_F = '<span>在线工程师 18 名</span><span class="tag ok">SLA 达标 94%</span>'

S06 = dict(
    id="06-service-dispatch", name="智能售后服务管理", en="FIELD SERVICE DISPATCH",
    nav=SVC_NAV, active="服务总览", crumb="服务总览 <em>/ 城东辖区</em>",
    tb=tb_right("2026 年 9 月", "岑柏年", "服务调度中心", "14"),
    side_f=SVC_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="待派工单", value="14", unit="单", tone="warn", desc="其中 <b>3 单</b>已接近 SLA 上限"),
            dict(label="今日完工", value="26", unit="单", tone="ok", desc="一次上门解决 22 单"),
            dict(label="SLA 达标", value="94", unit="%", tone="acc", desc="超时 2 单已升级处理"),
            dict(label="平均响应时长", value="46", unit="分钟", tone="ok", desc="较上月 <i>缩短 8 分钟</i>"),
        ]),
        # 地图 + 工程师列表
        '<div class="row" style="grid-template-columns:minmax(0,1.75fr) minmax(0,1fr)">'
        + panel("工程师与工单分布", map_panel(), sub="实时刷新 · 城东辖区",
                right=chip("按技能筛选", "filter") + chip("自动派单开关", "bolt", True))
        + panel("工程师状态", (
            '<div style="padding:8px 14px">'
            + "".join(
                '<div style="display:flex;align-items:center;gap:11px;padding:10px 2px;'
                'border-bottom:1px solid rgba(255,255,255,.04)">'
                '<span class="av" style="width:30px;height:30px;font-size:11.5px">%s</span>'
                '<div style="flex:1;min-width:0"><div style="font-size:12.5px;font-weight:500">%s</div>'
                '<div style="font-size:11px;color:var(--s-t3);margin-top:2px">%s</div></div>'
                '<div style="text-align:right"><div style="font-size:11px;color:var(--s-t3)">今日</div>'
                '<div style="font-size:13px;font-weight:600;font-family:\'Geist Mono\',monospace">%s</div></div>'
                "<div>%s</div></div>"
                % d for d in [
                    ("骆", "骆明轩", "复印机 · 网络打印", "4", tag("在途", "warn")),
                    ("温", "温子澄", "复印机 · 装订设备", "3", tag("在岗", "ok")),
                    ("禹", "禹嘉行", "网络打印 · 服务器", "5", tag("在途", "warn")),
                    ("钟", "钟亦舟", "复印机 · 耗材", "2", tag("在岗", "ok")),
                    ("柏", "柏仲言", "装订设备 · 网络", "3", tag("在岗", "ok")),
                    ("解", "解云舟", "网络打印 · 复印机", "4", tag("已完工", "mute")),
                ]
            )
            + "</div>"
        ), sub="共 18 名 · 显示前 6"),
        "</div>"
        + panel("工单流转", funnel([
            ("新建工单", "42"), ("已派单", "38"), ("已出发", "32"), ("已到场", "30"), ("已完工", "26"),
        ]), sub="今日 08:00 至 09:42", right=chip("查看超时工单", "alert-triangle")),
    ),
)

# ================================================== 06b 工单详情

S06B = dict(
    id="06b-work-order-detail", name="智能售后服务管理", en="FIELD SERVICE DISPATCH",
    nav=SVC_NAV, active="工单池", crumb="工单池 <em>/ WO-20260921-0142</em>",
    tb=tb_right("2026 年 9 月", "岑柏年", "服务调度中心", "14"),
    side_f=SVC_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:auto minmax(0,1fr);gap:16px;min-height:0">'
        '<div class="panel" style="flex-direction:row;align-items:center;padding:0 18px;height:76px">'
        '<div><div style="font-size:15.5px;font-weight:600;letter-spacing:-.012em">'
        'WO-20260921-0142 · 宁波睿达智能装备 · 报修</div>'
        '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px">'
        'MFP-C5580（序列号 AJ-8817062）· 客户 3 楼办公区 · 提单 08:36</div></div>'
        '<div style="margin-left:auto;display:flex;align-items:center;gap:22px">'
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">故障类型</div>'
        '<div style="margin-top:5px">' + tag("卡纸 · 反复报错", "warn") + "</div></div>"
        '<div style="text-align:right"><div style="font-size:11.5px;color:var(--s-t3)">剩余 SLA</div>'
        '<div style="font-size:20px;font-weight:600;font-family:\'Geist Mono\',monospace">2h 46m</div></div>'
        '<span class="chip acc">' + ic("current-location", 13) + "骆明轩 已出发" + "</span>"
        '<span class="chip">' + ic("clipboard-check", 13) + "填写服务报告" + "</span></div></div>"
        + '<div class="row" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr) 330px">'
        + panel("设备档案", (
            kv([
                ("客户", "<b>宁波睿达智能装备</b>"), ("安装地址", "<b>宁波市高新区研发园 3 号 3 楼</b>"),
                ("机型", "<b>MFP-C5580</b>"), ("序列号", "<b>AJ-8817062</b>"),
                ("装机日期", "<b>2025-03-18</b>"), ("保修状态", tag("延保中 · 至 2027-03", "ok")),
                ("整机读数", "<b>1,412,860 页</b>"), ("本月已修", "<b>2 次</b>"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:4px 16px 0"></div>'
            + '<div style="padding:14px 16px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:10px">历史服务记录</div>'
            + timeline([
                ("ok", "更换硒鼓组件", "09-08 · 温子澄 · 一次解决"),
                ("warn", "卡纸清理 · 更换搓纸轮", "08-21 · 骆明轩 · 复发 1 次"),
                ("ok", "定期保养", "07-30 · 钟亦舟 · 正常"),
            ])
            + "</div>"
        ), sub="一机一档"),
        panel("故障诊断与处理", (
            '<div style="padding:14px 16px">'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:10px">故障模式匹配</div>'
            + progress_rows([
                ("进纸机构磨损（历史高发）", 82, "匹配 82%"),
                ("传感器积尘", 46, "匹配 46%"),
                ("定影单元异常", 12, "匹配 12%"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:4px 0 12px"></div>'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:8px">知识库建议</div>'
            '<div style="background:var(--s-panel-2);border:1px solid var(--s-line);border-radius:9px;'
            'padding:12px;font-size:12.5px;color:var(--s-t2);line-height:1.7">'
            "同机型同故障共 14 例，其中 11 例为搓纸轮磨损。"
            "建议携带搓纸轮组件（备件号 <b>RF-3307</b>）与清洁工具。</div>"
            '<div style="margin-top:12px;display:flex;gap:8px">'
            + chip("推送排查手册", "book") + chip("申请备件", "package", True) + "</div></div>"
        ), sub="基于历史工单与知识库"),
        panel("处理记录", (
            '<div style="padding:14px 16px">'
            + timeline([
                ("ok", "客户报修", "08:36 · 扫码提交 · 附故障照片 2 张"),
                ("ok", "自动派单", "08:37 · 骆明轩（技能匹配 · 距离 4.2 km）"),
                ("acc", "工程师出发", "09:02 · 预计 09:26 到达"),
                ("mute", "到场签到", "待确认"),
                ("mute", "更换备件", "待填写"),
                ("mute", "客户签字确认", "待确认"),
            ])
            + "</div>"
        ), sub="全流程留痕"),
        "</div>",
        "</div>"
    ),
)

# ================================================== 07 AI 智能客服

CS_NAV = [
    ("客服工作台", ""), ("会话管理", "11"), ("知识库", ""), ("话术与政策", ""),
    ("渠道接入", ""), ("#设置", ""), ("机器人配置", ""),
]
CS_F = '<span>知识库条目 1,286</span><span class="tag ok">已同步</span>'

S07 = dict(
    id="07-customer-service", name="AI 智能客服", en="AI CONTACT CENTER",
    nav=CS_NAV, active="客服工作台", crumb="客服工作台 <em>/ 实时会话</em>",
    tb=tb_right("2026 年 9 月", "慕书瑶", "客服主管", "11"),
    side_f=CS_F, note=NOTE_TS,
    canvas=canvas(
        kpis([
            dict(label="今日会话", value="1,842", unit="次", tone="acc", desc="在线 386 · 电话 214 · 微信 1,242"),
            dict(label="AI 独立解决", value="1,426", unit="次", tone="ok", desc="未解决 416 次已回流知识库"),
            dict(label="转人工", value="416", unit="次", tone="warn", desc="其中 <b>38 次</b>为情绪升级"),
            dict(label="不满意会话", value="9", unit="次", tone="bad", desc="低于 3 分 · 已安排主管回访"),
        ]),
        # 会话列表 + 对话 + 右侧画像
        '<div class="row" style="grid-template-columns:300px minmax(0,1fr) 330px">'
        + panel("会话列表", (
            '<div style="padding:6px 10px">'
            + "".join(
                '<div style="display:flex;gap:10px;padding:10px;border-radius:9px;%s">'
                '<span class="av" style="width:28px;height:28px;font-size:11px">%s</span>'
                '<div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;gap:8px">'
                '<span style="font-size:12.5px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">%s</span>'
                '<span style="font-size:10.5px;color:var(--s-t3);font-family:\'Geist Mono\',monospace">%s</span></div>'
                '<div style="font-size:11.5px;color:var(--s-t3);margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">%s</div>'
                '<div style="margin-top:6px">%s</div></div></div>'
                % d for d in [
                    ("background:var(--s-acc-soft)", "韩", "韩清越", "09:41", "设备报错 E-102，客服已答复", tag("AI 接待中", "info")),
                    ("", "秦", "秦知远", "09:38", "要求工程师上门复核", tag("已转人工", "warn")),
                    ("", "苏", "苏亦辰", "09:34", "查询上月印量账单", tag("AI 接待中", "info")),
                    ("", "柏", "柏仲言", "09:30", "投诉配送延迟，情绪升级", tag("情绪升级", "bad")),
                    ("", "祁", "祁明昭", "09:26", "申请备用机更换", tag("已转人工", "warn")),
                    ("", "崔", "崔怀瑾", "09:21", "耗材更换周期咨询", tag("AI 接待中", "info")),
                    ("", "范", "范书棠", "09:14", "合同续签条款咨询", tag("已转人工", "warn")),
                    ("", "柏", "柏仲言", "09:08", "开发票信息修改", tag("已办结", "mute")),
                ]
            )
            + "</div>"
        ), sub="11 个进行中", right=chip("仅看转人工")),
        panel("对话", (
            '<div style="padding:14px 16px;display:flex;flex-direction:column;gap:12px;height:100%">'
            '<div style="display:flex;gap:10px"><span class="av" style="width:28px;height:28px;font-size:11px">苏</span>'
            '<div class="bub">你好，帮我查一下上个月我们公司的打印机印量账单，财务要核对。</div></div>'
            '<div style="display:flex;gap:10px;flex-direction:row-reverse">'
            '<span class="av" style="width:28px;height:28px;font-size:11px;background:var(--s-acc-soft);border-color:var(--s-acc-line);color:var(--s-acc)">AI</span>'
            '<div class="bub me">已查到贵单位 2026-09 周期账单：设备 MFP-C5580 共 4 台，'
            '本期印量 126,460 页，应付 ¥4,286.40。需要我把账单 PDF 发到财务邮箱吗？<div class="src">'
            + ic("book", 12) + "依据：合同 RT-2025-0168 · 计费规则 2026-07-01</div></div></div>"
            '<div style="display:flex;gap:10px"><span class="av" style="width:28px;height:28px;font-size:11px">苏</span>'
            '<div class="bub">发到 finance@haolian.com 就行。另外这台机器最近老卡纸，能安排人看看吗？</div></div>'
            '<div style="background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.28);'
            'border-radius:9px;padding:11px 13px;font-size:11.5px;color:#FCD34D;line-height:1.6">'
            + ic("alert-triangle", 13) + " 政策红线：涉及上门时效的承诺必须引用服务等级协议原文，"
            "不得由 AI 自行给出时限。</div>"
            '<div style="display:flex;gap:10px;flex-direction:row-reverse">'
            '<span class="av" style="width:28px;height:28px;font-size:11px;background:var(--s-acc-soft);border-color:var(--s-acc-line);color:var(--s-acc)">AI</span>'
            '<div class="bub me">账单已发送。卡纸问题已为您登记，'
            '服务等级协议约定：工作日内 4 小时响应、次工作日上门。是否需要现在创建工单？</div></div>'
            '<div style="margin-top:auto;display:flex;align-items:center;gap:10px;'
            'border-top:1px solid var(--s-line);padding-top:12px">'
            '<span class="chip acc">' + ic("message", 13) + "输入回复…" + "</span>"
            '<span class="chip">' + ic("message-chatbot", 13) + "AI 起草回复" + "</span>"
            '<span style="margin-left:auto"></span>'
            + chip("查看历史会话") + chip("转人工", "user", True) + "</div>"
            "</div>"
        ), sub="对话可全程回放"),
        panel("客户画像与建议", (
            '<div style="padding:14px 16px">'
            + kv([
                ("客户", "<b>杭州海联电子</b>"), ("合作年限", "<b>3 年 2 个月</b>"),
                ("在用设备", "<b>7 台</b>"), ("合同到期", "<b>2027-01-31</b>"),
                ("历史工单", "<b>24 单</b>"), ("服务评分", "<b>4.7 分</b>"),
            ])
            + '<div style="border-top:1px solid var(--s-line);margin:12px 0"></div>'
            '<div style="font-size:12.5px;color:var(--s-t2);margin-bottom:10px">AI 建议话术</div>'
            '<div style="background:var(--s-panel-2);border:1px solid var(--s-line);border-radius:9px;'
            'padding:12px;font-size:12.5px;color:var(--s-t2);line-height:1.7">'
            "该客户为高价值长期客户，近 90 天卡纸工单 3 次，"
            "建议在本次服务中主动提出预防性保养。</div>"
            '<div style="margin-top:14px;font-size:12.5px;color:var(--s-t2);margin-bottom:10px">'
            "未解决问题回流</div>"
            + timeline([
                ("warn", "上门时效承诺（38 次）", "已补充政策原文条目"),
                ("ok", "备用机申请流程（26 次）", "已加入知识库"),
                ("mute", "跨省配送费用（14 次）", "待业务确认"),
            ])
            + "</div>"
        ), sub="知识库 1,286 条"),
        "</div>"
    ),
)

# ================================================== 07b 知识库运营

S07B = dict(
    id="07b-knowledge-base", name="AI 智能客服", en="AI CONTACT CENTER",
    nav=CS_NAV, active="知识库", crumb="知识库 <em>/ 覆盖与回流</em>",
    tb=tb_right("2026 年 9 月", "慕书瑶", "客服主管", "11"),
    side_f=CS_F, note=NOTE_TS,
    canvas=(
        '<div style="flex:1;min-height:0;display:grid;grid-template-rows:100px minmax(0,1fr) 196px;gap:16px">'
        '<div class="kpis" style="grid-template-columns:repeat(4,minmax(0,1fr))">'
        '<div class="kpi ok"><div class="kpi-k">知识库覆盖</div><div class="kpi-v">82<u>%</u></div>'
        '<div class="kpi-d">较上月 <i>+6 个百分点</i></div></div>'
        '<div class="kpi warn"><div class="kpi-k">待补充条目</div><div class="kpi-v">34<u>条</u></div>'
        '<div class="kpi-d">来自未解决问题回流</div></div>'
        '<div class="kpi acc"><div class="kpi-k">答案溯源率</div><div class="kpi-v">100<u>%</u></div>'
        '<div class="kpi-d">每条回答均引用原文</div></div>'
        '<div class="kpi acc"><div class="kpi-k">答案采纳率</div><div class="kpi-v">96.4<u>%</u></div>'
        '<div class="kpi-d">客服采纳 AI 建议话术的比例</div></div>'
        "</div>"
        + '<div class="row" style="grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)">'
        + panel("未解决问题回流", table(
            [("问题主题", 34, ""), ("出现次数", 12, "num"), ("来源渠道", 14, ""),
             ("处理进展", 22, ""), ("状态", 18, "")],
            [
                ["上门服务时效怎么算", "38", "在线客服", "已补充协议原文条目", tag("已入库", "ok")],
                ["备用机申请流程", "26", "电话", "已加入知识库并验证", tag("已入库", "ok")],
                ["跨省配送是否收费", "14", "微信", "待业务部门确认口径", tag("待确认", "warn")],
                ["设备报错码 E-102 含义", "12", "在线客服", "已关联故障模式库", tag("已入库", "ok")],
                ["账号权限变更流程", "9", "邮件", "待补充审核节点说明", tag("待确认", "warn")],
                ["发票信息修改时限", "7", "电话", "已加入知识库", tag("已入库", "ok")],
                ["延保与保修的区别", "5", "在线客服", "条款冗长，待改写为问答", tag("改写中", "info")],
                ["月度账单争议处理", "4", "微信", "已补充对账流程", tag("已入库", "ok")],
            ]), sub="近 30 天共 34 条", right=chip("一键生成草稿", "bolt", True)),
        panel("知识库条目构成", donut(
            [("#22D3EE", 30.0, "产品手册", "386"),
             ("#60A5FA", 20.8, "售后政策", "268"),
             ("#FBBF24", 26.6, "故障手册", "342"),
             ("#34D399", 22.5, "历史工单", "290")],
            "1,286", "知识库条目"), sub="企业自有资料，非公开语料"),
        "</div>"
        + panel("答案溯源示例", (
            '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;padding:14px 18px">'
            '<div><div style="font-size:12.5px;color:var(--s-t3);margin-bottom:9px">客户提问</div>'
            '<div class="bub" style="max-width:none;margin:0">设备保修期内上门维修收不收费？</div></div>'
            '<div><div style="font-size:12.5px;color:var(--s-t3);margin-bottom:9px">AI 回答（附引用原文）</div>'
            '<div class="bub me" style="max-width:none;margin:0">'
            "保修期内非人为损坏的维修免收上门费与工时费，"
            "仅更换的配件按价目表计费。<div class=\"src\">"
            + ic("book", 12) + "《售后服务政策 V3.2》第 2.4 条 · 第 3 段</div></div></div>"
            "</div>"
        ), sub="涉及费用、责任、时效的回答一律引用原文", right=chip("查看引用规则")),
        "</div>"
    ),
)


SCREENS = [S01N, S01BN, S02N, S02BN, S03, S03B, S04, S04B, S05, S05B, S06, S06B, S07, S07B]


def build():
    done = []
    for s in SCREENS:
        can = s["canvas"]
        # 有的定义写成 canvas=(... + ...) 的元组，这里统一拼成字符串
        if isinstance(can, (tuple, list)):
            can = "".join(can)
        html = page(
            s["id"], s["name"], s["en"], s["nav"], s["active"],
            s["side_f"], s["crumb"], s["tb"], can, s["note"],
        )
        p = os.path.join(HERE, s["id"] + ".html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        done.append((s["id"] + ".html", len(can)))
    print("生成 %d 个界面稿：" % len(done))
    for d, n in done:
        flag = "  <-- 画布为空！" if n < 500 else ""
        print("  %-34s 画布 %5d 字符%s" % (d, n, flag))


if __name__ == "__main__":
    build()
