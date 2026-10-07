# -*- coding: utf-8 -*-
"""diag.py · 量化诊断：逐个界面稿测量各区块实际高度与内容溢出

输出每个界面的「画布高度 / 每个子块高度 / 内容是否溢出容器」，用于排查塌陷与空白。
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DIAG_JS = """
<script>
setTimeout(function () {
  function pick(sel, root) { return (root || document).querySelector(sel); }
  var L = [];
  ['html', 'body', '.win', '.app', '.side', '.main', '.tb', '.canvas'].forEach(function (s) {
    var el = s === 'html' ? document.documentElement : (s === 'body' ? document.body : pick(s));
    if (!el) { L.push(s + ' MISSING'); return; }
    var cs = getComputedStyle(el);
    L.push(s + ' h=' + Math.round(el.getBoundingClientRect().height)
      + ' clientH=' + el.clientHeight
      + ' scrollH=' + el.scrollHeight
      + ' display=' + cs.display + ' flex=' + cs.flex + ' minH=' + cs.minHeight
      + ' height=' + cs.height);
  });
  var c = pick('.canvas');
  var kids = [].slice.call(c.children);
  kids.forEach(function (ch, i) {
    var r = ch.getBoundingClientRect();
    L.push('C' + i + ' ' + ch.tagName.toLowerCase()
      + (ch.className ? '.' + String(ch.className).replace(/ /g, '.') : '')
      + ' h=' + Math.round(r.height) + ' scrollH=' + ch.scrollHeight
      + (ch.scrollHeight > ch.clientHeight + 2 ? ' OVERFLOW' : ''));
    var inner = [].slice.call(ch.children);
    inner.forEach(function (g, j) {
      if (g.getBoundingClientRect().height < 2) return;
      var gr = g.getBoundingClientRect();
      var p = g.classList.contains('panel') ? g : g.querySelector('.panel');
      L.push('  N' + i + j + ' ' + (g.classList.contains('panel') ? 'panel' : g.tagName.toLowerCase())
        + ' h=' + Math.round(gr.height)
        + (p ? ' scrollH=' + p.scrollHeight + (p.scrollHeight > p.clientHeight + 2 ? ' OVERFLOW' : '') : ''));
    });
  });
  document.title = 'DIAG ' + L.join(' ;; ');
}, 900);
</script>
"""


def main():
    names = sys.argv[1:] or sorted(
        f for f in os.listdir(HERE) if f.endswith(".html") and f[0].isdigit()
    )
    only = "--err" in names
    for fn in names:
        if fn == "--err":
            continue
        src = os.path.join(HERE, fn)
        raw = open(src, encoding="utf-8").read()
        # 临时文件必须放在同目录，否则 screen.css / sprite.js 的相对路径会失效
        tmp = os.path.join(HERE, "_diag_tmp.html")
        open(tmp, "w", encoding="utf-8").write(raw.replace("</body>", DIAG_JS + "</body>"))
        try:
            r = subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--hide-scrollbars", "--virtual-time-budget=3000",
                 "--window-size=1400,875", "--dump-dom", "file://" + tmp],
                capture_output=True, text=True, timeout=90,
            )
        finally:
            pass
        m = re.search(r"<title>DIAG (.*?)</title>", r.stdout, re.S)
        print("=" * 78)
        print(fn)
        if not m:
            print("  未取到诊断数据")
            continue
        for part in m.group(1).split(";;"):
            part = part.strip()
            if only and "OVERFLOW" not in part:
                continue
            print("  " + part)


if __name__ == "__main__":
    try:
        main()
    finally:
        t = os.path.join(HERE, "_diag_tmp.html")
        if os.path.exists(t):
            os.remove(t)
