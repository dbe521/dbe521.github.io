# -*- coding: utf-8 -*-
"""gen_lib.py · 系统界面示意图的 HTML 组件库

把界面拆成可复用组件，14 张图共用一套模板。
所有坐标与图表路径都在 Python 里算好，避免手写 SVG 出错。
"""

# ---------------------------------------------------------------- 基础件


def ic(name, w=None):
    s = ' style="width:%dpx;height:%dpx"' % (w, w) if w else ""
    return '<svg class="ic"%s><use href="#i-%s"></use></svg>' % (s, name)


def esc(t):
    return (
        str(t)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def tag(text, tone="mute"):
    return '<span class="tag %s">%s</span>' % (tone, esc(text))


# ---------------------------------------------------------------- KPI


def kpi(label, value, unit="", desc="", tone="acc", steps=None):
    """tone: acc / ok / warn / bad"""
    v = '<div class="kpi-v">%s%s</div>' % (
        esc(value),
        "<u>%s</u>" % esc(unit) if unit else "",
    )
    d = '<div class="kpi-d">%s</div>' % desc if desc else ""
    st = ""
    if steps:
        done, cur, total = steps
        cells = []
        for i in range(total):
            if i < done:
                cells.append('<i class="d"></i>')
            elif i == done:
                cells.append('<i class="c"></i>')
            else:
                cells.append("<i></i>")
        st = '<div class="kpi-steps">%s</div>' % "".join(cells)
    size = ' style="font-size:19px;font-weight:500"' if len(str(value)) > 5 else ""
    v = v.replace('<div class="kpi-v">', '<div class="kpi-v"%s>' % size)
    return (
        '<div class="kpi %s"><div class="kpi-k">%s</div>%s%s%s</div>'
        % (tone, esc(label), v, d, st)
    )


def kpis(items):
    return '<div class="kpis">%s</div>' % "".join(kpi(**it) for it in items)


# ---------------------------------------------------------------- 面板


def panel(title, body, sub="", right="", cls="", hd=True):
    head = ""
    if hd:
        head = '<div class="p-hd"><h3>%s</h3>%s%s</div>' % (
            esc(title),
            '<span class="sub">%s</span>' % esc(sub) if sub else "",
            '<div class="right">%s</div>' % right if right else "",
        )
    return '<div class="panel %s">%s<div class="p-bd">%s</div></div>' % (
        cls,
        head,
        body,
    )


def chip(text, icon=None, acc=False):
    return '<span class="chip%s">%s%s</span>' % (
        " acc" if acc else "",
        ic(icon, 13) if icon else "",
        esc(text),
    )


# ---------------------------------------------------------------- 表格


def table(cols, rows, compact=False):
    """cols: [(标题, 宽度%, 对齐)]  rows: [[单元格HTML, ...]]"""
    th = "".join(
        '<th%s%s>%s</th>'
        % (
            ' class="tb-num"' if (len(c) > 2 and c[2] == "num") else "",
            ' style="width:%s%%"' % c[1] if len(c) > 1 and c[1] else "",
            esc(c[0]),
        )
        for c in cols
    )
    trs = []
    for r in rows:
        tds = []
        for i, cell in enumerate(r):
            cls = ' class="num"' if (len(cols[i]) > 2 and cols[i][2] == "num") else ""
            tds.append("<td%s>%s</td>" % (cls, cell))
        trs.append("<tr>%s</tr>" % "".join(tds))
    return "<table%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (
        ' class="compact"' if compact else "",
        th,
        "".join(trs),
    )


# ---------------------------------------------------------------- 环形图


def donut(segments, center_v, center_s, size=156):
    """segments: [(颜色, 百分比, 名称, 数值)]"""
    stops = []
    acc = 0.0
    for c, p, _n, _v in segments:
        stops.append("%s %s%% %s%%" % (c, round(acc, 1), round(acc + p, 1)))
        acc += p
    grad = "conic-gradient(from -90deg, %s)" % ", ".join(stops)
    legend = "".join(
        '<div class="lg"><i style="background:%s"></i>%s<u>%s</u></div>' % (c, esc(n), esc(v))
        for c, _p, n, v in segments
    )
    return (
        '<div style="display:flex;flex-direction:column;justify-content:center;'
        'gap:20px;padding:16px 18px;height:100%%">'
        '<div style="display:flex;justify-content:center">'
        '<div class="donut" style="background:%s;width:%dpx;height:%dpx">'
        '<em><span><b>%s</b><s>%s</s></span></em></div></div>'
        '<div class="legend">%s</div></div>'
    ) % (grad, size, size, esc(center_v), esc(center_s), legend)


# ---------------------------------------------------------------- 面积图


def _area(points, y0_bottom, floor=150.0):
    """points: [(x, y)] 由高到低；返回多边形点串"""
    fwd = " ".join("%g,%g" % (x, y) for x, y in points)
    back = " ".join("%g,%g" % (x, y) for x, y in reversed(points))
    return "%s %g,%g %g,%g %s" % (
        fwd,
        points[-1][0],
        floor,
        points[0][0],
        floor,
        back,
    )


def area_chart(series, ylabels, xlabels, vmax, height=150, top=10, gx0=44, gx1=1180):
    """分层绘制：先铺填充 → 再画网格线与坐标 → 最后描顶线。
    （顺序很重要：填充若盖在网格线上，整图会糊成一块实心色块）
    """
    n = len(series[0][2])
    step = (gx1 - gx0) / (n - 1)
    xs = [gx0 + step * i for i in range(n)]

    def yv(v):
        return top + (1 - v / float(vmax)) * (height - top)

    # 1) 填充层
    fills = ""
    if len(series) == 1:
        pts = [(xs[i], yv(v)) for i, v in enumerate(series[0][2])]
        fills += '<polygon fill="rgba(%s)" stroke="none" points="%s"/>' % (
            series[0][4], _area(pts, height)
        )
    else:
        base = [(xs[i], height) for i in range(n)]
        for s in series:
            top_pts = [(xs[i], yv(s[2][i])) for i in range(n)]
            poly = " ".join("%g,%g" % p for p in top_pts)
            back = " ".join("%g,%g" % p for p in reversed(base))
            fills += '<polygon fill="rgba(%s)" stroke="none" points="%s %s"/>' % (
                s[4], poly, back
            )
            base = top_pts

    # 2) 网格线与坐标文字
    grid = ""
    for i, lab in enumerate(ylabels):
        y = top + (height - top) * i / (len(ylabels) - 1)
        grid += '<line class="gridline" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (gx0, y, gx1, y)
        grid += '<text class="axis" x="4" y="%g">%s</text>' % (y + 3, esc(lab))
    xl = "".join(
        '<text class="axis" x="%g" y="%g" text-anchor="%s">%s</text>'
        % (x, height + 22, a, esc(t))
        for x, t, a in xlabels
    )

    # 3) 顶线层（只描线不填充，保证线条清晰）
    lines = ""
    for s in series:
        pts = " ".join("%g,%g" % (xs[i], yv(s[2][i])) for i in range(n))
        lines += (
            '<polyline fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round" stroke-linecap="round" points="%s"/>'
            % (s[0], s[1], pts)
        )

    return (
        '<svg class="chart" viewBox="0 0 1180 180" style="height:100%%">%s%s%s%s</svg>'
        % (fills, grid, lines, xl)
    )


def legend_inline(items):
    return "".join(
        '<span class="lg" style="font-size:11.5px"><i style="background:%s"></i>%s</span>'
        % (c, esc(t))
        for c, t in items
    )


# ---------------------------------------------------------------- 柱状图


def bar_chart(cats, values, ylabels, vmax, gx0=44, gx1=1180, top=12, height=150,
              color="#22D3EE", values2=None, color2="#FBBF24"):
    """单系列或双系列柱状图（values2 非空时按组并列）"""
    n = len(values)
    span = (gx1 - gx0) / float(n)
    two = values2 is not None
    bw = min(26.0 if two else 38.0, span * (0.28 if two else 0.5))
    grid = ""
    for i, lab in enumerate(ylabels):
        y = top + (height - top) * i / (len(ylabels) - 1)
        grid += '<line class="gridline" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (gx0, y, gx1, y)
        grid += '<text class="axis" x="4" y="%g">%s</text>' % (y + 3, esc(lab))

    def draw(v, cx, c):
        h = max(2.0, (v / float(vmax)) * (height - top))
        return '<rect x="%g" y="%g" width="%g" height="%g" rx="4" fill="%s" opacity="0.92"/>' % (
            cx - bw / 2, height - h, bw, h, c
        )

    bars = ""
    for i, v in enumerate(values):
        cx = gx0 + span * (i + 0.5)
        if two:
            off = bw * 0.62
            bars += draw(values2[i], cx - off, color2)
            bars += draw(v, cx + off, color)
        else:
            bars += draw(v, cx, color)
        bars += '<text class="axis" x="%g" y="%g" text-anchor="middle" style="font-size:11px">%s</text>' % (
            cx, height + 20, esc(cats[i])
        )
    return '<svg class="chart" viewBox="0 0 1180 180" style="height:100%%">%s%s</svg>' % (grid, bars)


# ---------------------------------------------------------------- 漏斗


def funnel(stages, rgb="34,211,238"):
    """用 HTML 实现（不用 SVG），这样在窄面板里也能自适应、文字不糊。"""
    n = len(stages)
    rows = ""
    for i, (name, val) in enumerate(stages):
        w = 100 - i * (44.0 / max(1, n - 1))
        a = round(0.92 - i * 0.15, 2)
        rows += (
            '<div style="width:%g%%;margin:0 auto;height:40px;border-radius:8px;'
            'background:rgba(%s,%s);display:flex;align-items:center;'
            'justify-content:space-between;padding:0 14px;font-size:12.5px;'
            'color:#07141B;font-weight:500">'
            "<span>%s</span>"
            "<span style=\"font-family:'Geist Mono',monospace\">%s</span></div>"
        ) % (w, rgb, a, esc(name), esc(val))
    return '<div style="padding:16px;display:flex;flex-direction:column;gap:8px">%s</div>' % rows


# ---------------------------------------------------------------- 简笔地图


def map_panel(dark=True):
    """一张抽象城市底图 + 三类点位，用于调度类界面。"""
    pins = [
        (210, 120, "ok"), (268, 78, "ok"), (330, 150, "busy"), (398, 96, "ok"),
        (452, 168, "busy"), (520, 108, "ok"), (586, 62, "ok"), (648, 140, "busy"),
        (712, 92, "ok"), (768, 158, "busy"), (836, 104, "ok"), (896, 60, "ok"),
        (958, 132, "busy"), (1020, 86, "ok"), (1082, 148, "busy"), (300, 210, "ok"),
        (470, 232, "busy"), (642, 214, "ok"), (812, 236, "busy"), (982, 206, "ok"),
    ]
    roads = (
        '<rect x="0" y="0" width="1180" height="270" fill="#121821"/>'
        '<path d="M0 74 H1180" stroke="#39424F" stroke-width="4"/>'
        '<path d="M0 196 H1180" stroke="#39424F" stroke-width="3"/>'
        '<path d="M150 0 V270" stroke="#39424F" stroke-width="4"/>'
        '<path d="M420 0 V270" stroke="#39424F" stroke-width="3"/>'
        '<path d="M700 0 V270" stroke="#39424F" stroke-width="4"/>'
        '<path d="M980 0 V270" stroke="#39424F" stroke-width="3"/>'
        '<path d="M0 136 C200 120 260 176 420 150 S760 108 1180 140" stroke="#2A3644" stroke-width="8" fill="none"/>'
        '<rect x="60" y="88" width="76" height="40" rx="5" fill="#1B232E"/>'
        '<rect x="188" y="92" width="52" height="34" rx="5" fill="#1B232E"/>'
        '<rect x="470" y="86" width="120" height="44" rx="5" fill="#1B232E"/>'
        '<rect x="820" y="150" width="130" height="40" rx="5" fill="#1B232E"/>'
        '<rect x="200" y="204" width="150" height="46" rx="5" fill="#16262E"/>'
        '<rect x="560" y="204" width="110" height="46" rx="5" fill="#16262E"/>'
        '<rect x="880" y="206" width="90" height="44" rx="5" fill="#16262E"/>'
    )
    colors = {"ok": "#34D399", "busy": "#F87171"}
    pin_svg = ""
    for x, y, kind in pins:
        c = colors.get(kind, "#34D399")
        pin_svg += (
            '<circle cx="%d" cy="%d" r="11" fill="%s" opacity="0.22"/>'
            '<circle cx="%d" cy="%d" r="6" fill="%s" stroke="#0F1319" stroke-width="1.5"/>'
            % (x, y, c, x, y, c)
        )
    return (
        '<div style="position:relative;height:100%%;background:#0F1319;border-radius:0">'
        '<svg viewBox="0 0 1180 270" preserveAspectRatio="xMidYMid slice" style="width:100%%;height:100%%">'
        "%s%s</svg>"
        '<div style="position:absolute;left:14px;bottom:12px;display:flex;gap:14px;'
        'background:rgba(10,13,18,.85);border:1px solid rgba(255,255,255,.08);'
        'padding:8px 12px;border-radius:9px">'
        '<span class="lg" style="font-size:11px"><i style="background:#34D399"></i>在岗</span>'
        '<span class="lg" style="font-size:11px"><i style="background:#F87171"></i>在途</span>'
        "</div></div>"
    ) % (roads, pin_svg)


# ---------------------------------------------------------------- 小件


def pipeline(steps):
    """数据处理流水线（横向流程，带箭头分隔）
    steps: [(序号, 名称, 产出说明)]
    """
    cells = []
    for i, (no, name, out) in enumerate(steps):
        cells.append(
            '<div style="flex:1;min-width:0">'
            '<div style="display:flex;align-items:center;gap:8px;margin-bottom:9px">'
            '<span style="width:23px;height:23px;border-radius:7px;background:var(--s-acc-soft);'
            "border:1px solid var(--s-acc-line);color:var(--s-acc);font-size:11.5px;"
            "display:grid;place-items:center;font-family:'Geist Mono',monospace;flex:none\">%s</span>"
            '<span style="font-size:13px;font-weight:500;white-space:nowrap">%s</span>'
            "</div>"
            '<div style="font-size:11.5px;color:var(--s-t3);line-height:1.55">%s</div>'
            "</div>" % (esc(no), esc(name), esc(out))
        )
        if i < len(steps) - 1:
            cells.append(
                '<div style="flex:none;margin-top:9px;color:var(--s-t3);opacity:.65">'
                + ic("arrow-narrow-right", 16)
                + "</div>"
            )
    return (
        '<div style="display:flex;align-items:flex-start;gap:10px;padding:19px 18px 17px">%s</div>'
        % "".join(cells)
    )


def chan_card(title, count, unit, where, effect, tone="acc"):
    """人工裁决通道卡片"""
    return (
        '<div style="background:var(--s-panel-2);border:1px solid var(--s-line);'
        'border-radius:10px;padding:13px 14px;margin-bottom:11px">'
        '<div style="display:flex;align-items:center;gap:9px">'
        '<span style="font-size:12.5px;font-weight:500">%s</span>'
        '<span style="margin-left:auto;font-size:17px;font-weight:600;'
        "font-family:'Geist Mono',monospace;color:var(--s-acc)\">%s<u style=\"font-size:11px;"
        'font-weight:400;color:var(--s-t3);text-decoration:none;margin-left:3px">%s</u></span>'
        "</div>"
        '<div style="font-size:11.5px;color:var(--s-t3);line-height:1.6;margin-top:8px">'
        "填写位置：%s<br>生效方式：%s</div></div>"
        % (esc(title), esc(count), esc(unit), esc(where), esc(effect))
    )


def _stage_state(i, cur):
    """返回 (状态名, 主色, 边框色, 底色, 透明度)"""
    if i < cur:
        return "已完成", "#34D399", "rgba(52,211,153,.34)", "rgba(52,211,153,.07)", 1
    if i == cur:
        return "当前阶段", "#22D3EE", "rgba(34,211,238,.5)", "rgba(34,211,238,.13)", 1
    if i == cur + 1:
        return "下一阶段", "#FBBF24", "rgba(251,191,36,.5)", "rgba(251,191,36,.12)", 1
    return "待开始", "#6C7484", "var(--s-line)", "transparent", 0.72


def stage_board(stages, cur):
    """横向递进式阶段看板（项目组合视图）
    stages: [(阶段名, 数量文本, 执行点, 关键点)]
    当前阶段与下一阶段额外展示执行点与关键点，并高亮配色。
    布局刻意压扁：圆点+序号+阶段名同一行，避免整块被面板截断。
    """
    cells = []
    for i, (name, cnt, act, key) in enumerate(stages):
        st, c, bd, bg, op = _stage_state(i, cur)
        detail = ""
        if i in (cur, cur + 1):
            detail = (
                '<div style="margin-top:10px;padding-top:8px;border-top:1px dashed %s">'
                '<div style="font-size:11px;color:var(--s-t2);line-height:1.55">'
                '<span style="color:%s">执行点</span> · %s</div>'
                '<div style="font-size:11px;color:var(--s-t2);line-height:1.55;margin-top:5px">'
                '<span style="color:%s">关键点</span> · %s</div>'
                "</div>" % (bd, c, esc(act), c, esc(key))
            )
        cells.append(
            '<div style="flex:1;min-width:0;opacity:%s">'
            '<div style="display:flex;align-items:center;gap:7px;margin-bottom:9px">'
            '<span style="width:9px;height:9px;border-radius:50%%;background:%s;flex:none%s"></span>'
            '<span style="font-size:9.5px;color:var(--s-t3);font-family:\'Geist Mono\',monospace">%02d</span>'
            '<span style="font-size:12.5px;font-weight:500;white-space:nowrap;overflow:hidden;'
            'text-overflow:ellipsis">%s</span></div>'
            '<div style="font-size:11px;color:var(--s-t3);line-height:1.5;margin-bottom:9px">%s</div>'
            '<div><span class="tagch" style="border-color:%s;background:%s;color:%s">%s</span></div>%s'
            "</div>" % (
                op, c,
                ";box-shadow:0 0 0 3px rgba(34,211,238,.16)" if i == cur else "",
                i + 1, esc(name), esc(cnt), bd, bg, c, st, detail,
            )
        )
    return (
        '<div style="display:flex;align-items:stretch;gap:13px;padding:16px 18px">%s</div>'
        % "".join(cells)
    )


def stage_flow(stages, cur):
    """竖向递进阶段流（单项目详情视图）
    stages: [(阶段名, _, 执行点, 关键点, 备注)]
    只对「当前阶段」与「下一阶段」展开执行点 / 关键点，其余阶段压成一行，
    否则 8 段全展开会超出面板高度被截断。
    """
    rows = []
    n = len(stages)
    for i, item in enumerate(stages):
        name, act, key, memo = item[0], item[2], item[3], item[4]
        st, c, bd, bg, op = _stage_state(i, cur)
        last = i == n - 1
        badge = ""
        if i == cur:
            badge = ('<span class="tagch" style="border-color:rgba(34,211,238,.5);'
                     'background:rgba(34,211,238,.13);color:#67E8F9">当前阶段</span>')
        elif i == cur + 1:
            badge = ('<span class="tagch" style="border-color:rgba(251,191,36,.5);'
                     'background:rgba(251,191,36,.12);color:#FCD34D">下一阶段</span>')
        detail = ""
        if i in (cur, cur + 1):
            detail = (
                '<div style="margin-top:9px;padding:9px 11px;background:rgba(255,255,255,.03);'
                'border:1px solid var(--s-line);border-radius:8px">'
                '<div style="font-size:11.5px;color:var(--s-t2);line-height:1.6">'
                '<span style="color:%s">执行点</span> · %s</div>'
                '<div style="font-size:11.5px;color:var(--s-t2);line-height:1.6;margin-top:4px">'
                '<span style="color:%s">关键点</span> · %s</div></div>' % (c, esc(act), c, esc(key))
            )
        rows.append(
            '<div style="display:flex;gap:13px">'
            '<div style="flex:none;width:16px;display:flex;flex-direction:column;align-items:center">'
            '<span style="width:11px;height:11px;border-radius:50%%;background:%s;margin-top:14px;flex:none%s"></span>'
            "%s</div>"
            '<div style="flex:1;min-width:0;padding-bottom:%s">'
            '<div style="border:1px solid %s;background:%s;border-radius:10px;padding:10px 14px;opacity:%s">'
            '<div style="display:flex;align-items:center;gap:9px">'
            '<span style="font-size:9.5px;color:var(--s-t3);font-family:\'Geist Mono\',monospace">%02d</span>'
            '<span style="font-size:13px;font-weight:500">%s</span>%s'
            '<span style="margin-left:auto;font-size:11px;color:var(--s-t3)">%s</span></div>%s</div>'
            "</div></div>" % (
                c, ";box-shadow:0 0 0 3px rgba(34,211,238,.16)" if i == cur else "",
                "" if last else '<span style="flex:1;width:1px;background:var(--s-line);margin-top:5px"></span>',
                "2" if last else "9",
                bd, bg, op, i + 1, esc(name), badge, esc(memo), detail,
            )
        )
    return '<div style="padding:14px 18px">%s</div>' % "".join(rows)


def kv(items):
    return '<dl class="kv" style="padding:14px 16px">%s</dl>' % "".join(
        "<dt>%s</dt><dd>%s</dd>" % (esc(k), v) for k, v in items
    )


def timeline(items):
    """items: [(色调, 标题, 说明)]  色调: ok/acc/mute"""
    return '<div class="timeline" style="padding:12px 16px">%s</div>' % "".join(
        '<div class="tl"><span class="tl-i %s"></span><div><div class="tl-t">%s</div>'
        '<div class="tl-d">%s</div></div></div>' % (t, esc(k), esc(d))
        for t, k, d in items
    )


def progress_rows(items):
    """items: [(名称, 百分比, 数值文本)]"""
    out = ""
    for name, pct, val in items:
        out += (
            '<div style="padding:9px 0">'
            '<div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:7px">'
            '<span style="color:var(--s-t2)">%s</span>'
            '<span style="color:var(--s-t1);font-family:Geist Mono,monospace">%s</span></div>'
            '<div class="bar"><i style="width:%s%%"></i></div></div>'
        ) % (esc(name), esc(val), pct)
    return '<div style="padding:10px 16px">%s</div>' % out


def stat_row(items):
    """items: [(标签, 数值, 单位)]"""
    return '<div class="stat-row" style="padding:14px 16px">%s</div>' % "".join(
        '<div class="stat"><div class="stat-k">%s</div><div class="stat-v">%s%s</div></div>'
        % (esc(k), esc(v), "<u>%s</u>" % esc(u) if u else "")
        for k, v, u in items
    )


def steps_bar(items):
    """横向步骤：[(图标, 标题, 说明)]"""
    out = ""
    for i, (icon_name, t, d) in enumerate(items):
        out += (
            '<div style="flex:1;padding:0 10px;position:relative">'
            '<div style="display:flex;align-items:center;gap:9px;margin-bottom:9px">'
            '<span style="width:26px;height:26px;border-radius:8px;background:var(--s-acc-soft);'
            'border:1px solid var(--s-acc-line);color:var(--s-acc);display:grid;place-items:center">'
            "%s</span>"
            '<span style="font-size:12.5px;font-weight:500">%s</span></div>'
            '<div style="font-size:11.5px;color:var(--s-t3);line-height:1.55">%s</div>'
            "</div>"
        ) % (ic(icon_name, 15), esc(t), esc(d))
    return '<div style="display:flex;padding:16px 6px">%s</div>' % out


# ---------------------------------------------------------------- 整页


def page(screen_id, system_name, system_en, nav, nav_active, side_f, crumb, tb_right, canvas, note_right):
    """参数顺序与下面模板里的 %s 占位符严格一一对应，改动时务必同步两边。"""
    def nav_item(n):
        if n[0].startswith("#"):
            return '<div class="nav-g mono">%s</div>' % esc(n[0][1:])
        return (
            '<a class="nav-a%s">%s%s%s</a>'
            % (
                " on" if n[0] == nav_active else "",
                '<span class="nav-d"></span>',
                esc(n[0]),
                '<span class="nav-b">%s</span>' % esc(n[1])
                if len(n) > 1 and n[1]
                else "",
            )
        )

    nav_html = "".join(nav_item(n) for n in nav)
    return """<!doctype html>
<html lang="zh-CN" data-theme="dark" data-screen="%s">
<head>
<meta charset="utf-8">
<title>%s（界面示意）</title>
<link rel="stylesheet" href="screen.css">
</head>
<body>
<script src="../assets/icons/sprite.js"></script>
<div class="win">
  <div class="app">
    <aside class="side">
      <div class="logo">
        <span class="logo-i">%s</span>
        <div><div class="logo-t">%s</div><div class="logo-s mono">%s</div></div>
      </div>
      <nav class="nav">%s</nav>
      <div class="side-f">%s</div>
    </aside>
    <div class="main">
      <div class="tb">
        <div class="tb-crumb">%s</div>
        <div class="tb-search">%s搜索客户、设备编号、工单号</div>
        <div class="tb-right">%s</div>
      </div>
      <div class="canvas">%s</div>
    </div>
  </div>
  <div class="note"><b>系统界面示意</b>·数据为演示样例，不代表实际交付效果<u>%s</u></div>
</div>
</body>
</html>
""" % (
        screen_id,                 # 1  data-screen
        esc(system_name),          # 2  title
        ic(nav_icon(system_name), 17),  # 3  logo 图标
        esc(system_name),          # 4  logo 主标
        esc(system_en),            # 5  logo 副标
        nav_html,                  # 6  侧栏导航
        side_f,                    # 7  侧栏底栏
        crumb,                     # 8  顶部面包屑
        ic("search", 13),          # 9  搜索框图标
        tb_right,                  # 10 顶部右侧
        canvas,                    # 11 画布
        note_right,                # 12 底部标注右侧
    )


def nav_icon(system_name):
    m = {
        "AI 财务超级助理": "calculator",
        "AI 项目成交推进系统": "layout-kanban",
        "AI 企业经营决策中心": "layout-dashboard",
        "智能打印管控": "printer",
        "智能抄表及账单系统": "gauge",
        "智能售后服务管理": "tool",
        "AI 智能客服": "message-chatbot",
    }
    return m.get(system_name, "layout-dashboard")
