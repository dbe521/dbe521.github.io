# -*- coding: utf-8 -*-
"""render.py · 把 _screens 下的界面稿渲染成站点用的图片

输出：../assets/img/{场景}-{overview|detail}[.light].webp
深色版默认生成；传 --light 可生成浅色版（需先给 screen.css 加浅色令牌块）
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "assets", "img"))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VENV_PY = "/Users/tk/.workbuddy/binaries/python/envs/default/bin/python"

# 界面稿 id -> 站点里使用的图片名（与 content.js 的场景 id 对齐）
MAP = {
    "01-ai-finance-overview": "ai-finance-overview",
    "01b-ai-finance-detail": "ai-finance-detail",
    "02-project-overview": "project-management-overview",
    "02b-project-detail": "project-management-detail",
    "03-biz-cockpit": "business-workbench-overview",
    "03b-metric-drill": "business-workbench-detail",
    "04-print-control": "print-control-overview",
    "04b-print-archive": "print-control-detail",
    "05-meter-billing": "meter-billing-overview",
    "05b-billing-detail": "meter-billing-detail",
    "06-service-dispatch": "service-management-overview",
    "06b-work-order-detail": "service-management-detail",
    "07-customer-service": "ai-customer-service-overview",
    "07b-knowledge-base": "ai-customer-service-detail",
}

W, H = 1400, 875
SCALE = 2


def preflight(path):
    """渲染前结构自检：div 是否配对。之前因画布包裹层漏一个 </div>，
    导致页脚被挤进侧栏（宽度 200px 而非 1400px），肉眼很难发现。"""
    import re
    s = open(path, encoding="utf-8").read()
    if '<div class="canvas">' not in s:
        return "缺 canvas"
    region = s.split('<div class="canvas">', 1)[1].split('<div class="note">')[0]
    d = len(re.findall(r"<div[\s>]", region)) - len(re.findall(r"</div>", region))
    # 区域含 canvas / main / app 三个收尾标签，故差应为 -3
    if d != -3:
        return "div 不配对（差 %d，应为 -3，说明画布内多 %d 个未闭合 div）" % (d, -3 - d)
    return ""


def render(src_html, png_path, theme=None):
    url = "file://" + src_html
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=%d" % SCALE,
        "--virtual-time-budget=6000",
        "--window-size=%d,%d" % (W, H),
        "--screenshot=" + png_path, url,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def to_webp(png_path, webp_path):
    code = (
        "from PIL import Image\n"
        "import os\n"
        "im = Image.open(%r)\n"
        "im.save(%r, 'WEBP', quality=84, method=6)\n"
        "print(os.path.getsize(%r))\n" % (png_path, webp_path, webp_path)
    )
    r = subprocess.run([VENV_PY, "-c", code], capture_output=True, text=True, timeout=120)
    return int(r.stdout.strip() or 0)


def main():
    light = "--light" in sys.argv
    suffix = ".light" if light else ""
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for html_id, out_name in MAP.items():
        src = os.path.join(HERE, html_id + ".html")
        if not os.path.exists(src):
            print("  跳过（缺文件）:", html_id)
            continue
        warn = preflight(src)
        if warn:
            print("  !! %-34s %s" % (html_id, warn))
        png = os.path.join("/tmp", out_name + suffix + ".png")
        webp = os.path.join(OUT, out_name + suffix + ".webp")
        render(src, png)
        size = to_webp(png, webp)
        total += size
        os.remove(png)
        print("  %-34s %5.0f KB" % (out_name + suffix + ".webp", size / 1024.0))
    print("完成 %d 张 · 合计 %.1f MB" % (len(MAP), total / 1048576.0))


if __name__ == "__main__":
    main()
