/* ==========================================================================
   app.js  ·  渲染引擎 / 主题切换 / 交互 / 灯箱
   --------------------------------------------------------------------------
   一般不需要修改这个文件。改文案请改 content.js。
     1. 颜色系统：三套皮肤下的场景色解析与透明层推导
     2. 渲染：首页与 7 个详情页（含系统界面图、决策人三问、实施案例）
     3. 交互：主题切换、滚动进场、导航高亮、图片灯箱
   ========================================================================== */

(function () {
  "use strict";

  var S = window.SITE;
  var D = document;
  var TH_KEY = "sc-theme";
  var THEMES = ["dark", "light", "mono"];
  var U = S.ui;

  /* ======================================================================
     一、通用工具
     ====================================================================== */

  var ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  function esc(v) {
    return String(v === undefined || v === null ? "" : v).replace(/[&<>"']/g, function (c) {
      return ESC_MAP[c];
    });
  }
  function isBlank(v) {
    return v === undefined || v === null || String(v).trim() === "";
  }
  function txt(v) {
    return isBlank(v) ? '<span class="tbd">' + esc(U.tbd) + "</span>" : esc(v);
  }
  function icon(name, cls) {
    return (
      '<svg class="ic' + (cls ? " " + cls : "") +
      '" aria-hidden="true" focusable="false"><use href="#i-' + esc(name) + '"></use></svg>'
    );
  }
  function pct(a, b) {
    var x = parseFloat(a), y = parseFloat(b);
    if (!isFinite(x) || !isFinite(y) || x <= 0) return "-";
    return "↓" + Math.round((1 - y / x) * 100) + "%";
  }

  /* ======================================================================
     二、颜色系统
     ====================================================================== */

  function hex2rgb(h) {
    h = String(h || "").replace("#", "").trim();
    if (h.length === 3) h = h.charAt(0) + h.charAt(0) + h.charAt(1) + h.charAt(1) + h.charAt(2) + h.charAt(2);
    if (h.length !== 6 || /[^0-9a-fA-F]/.test(h)) return [null, null, null];
    return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)];
  }

  function rgba(hex, a) {
    var c = hex2rgb(hex);
    if (c[0] === null) return "rgba(128,128,128," + a + ")";
    return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a + ")";
  }

  function desat(hex, amt) {
    var c = hex2rgb(hex);
    if (c[0] === null) return hex;
    var r = c[0] / 255, g = c[1] / 255, b = c[2] / 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var l = (max + min) / 2, s = 0, hue = 0;
    if (max !== min) {
      var d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      if (max === r) hue = (g - b) / d + (g < b ? 6 : 0);
      else if (max === g) hue = (b - r) / d + 2;
      else hue = (r - g) / d + 4;
      hue /= 6;
    }
    s = Math.max(0, s * (1 - amt));
    function h2(p, q, t) {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }
    var q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    var out = s === 0 ? [l, l, l] : [h2(p, q, hue + 1 / 3), h2(p, q, hue), h2(p, q, hue - 1 / 3)];
    return (
      "#" +
      out
        .map(function (v) {
          var n = Math.round(Math.max(0, Math.min(1, v)) * 255).toString(16);
          return n.length < 2 ? "0" + n : n;
        })
        .join("")
    );
  }

  function curTheme() {
    var t = D.documentElement.getAttribute("data-theme");
    return THEMES.indexOf(t) >= 0 ? t : "dark";
  }

  function paint(el, hex) {
    var isDark = curTheme() === "dark";
    if (curTheme() === "mono") hex = desat(hex, 0.35);
    el.style.setProperty("--c", hex);
    el.style.setProperty("--c-soft", rgba(hex, isDark ? 0.15 : 0.1));
    el.style.setProperty("--c-line", rgba(hex, isDark ? 0.32 : 0.26));
    el.style.setProperty("--c-wash", rgba(hex, isDark ? 0.06 : 0.04));
  }

  var pageAccent = { d: null, l: null };

  function applyColors() {
    var isDark = curTheme() === "dark";
    var sc = isDark ? pageAccent.d : pageAccent.l;
    if (sc) {
      if (curTheme() === "mono") sc = desat(sc, 0.35);
      var root = D.documentElement;
      root.style.setProperty("--accent", sc);
      root.style.setProperty("--accent-ink", isDark ? "#08090C" : "#FCFCFD");
      root.style.setProperty("--accent-soft", rgba(sc, isDark ? 0.15 : 0.1));
      root.style.setProperty("--accent-line", rgba(sc, isDark ? 0.32 : 0.26));
      root.style.setProperty("--accent-wash", rgba(sc, isDark ? 0.06 : 0.04));
    }
    var list = D.querySelectorAll("[data-cd]");
    for (var i = 0; i < list.length; i++) {
      var el = list[i];
      paint(el, isDark ? el.getAttribute("data-cd") : el.getAttribute("data-cl"));
    }
  }

  /* ======================================================================
     三、导航与页脚
     ====================================================================== */

  function navHTML(activeId) {
    var links = S.sections
      .map(function (s) {
        var on = s.id === activeId ? " on" : "";
        return '<a class="nav-a' + on + '" href="index.html#' + esc(s.id) + '">' + esc(s.title) + "</a>";
      })
      .join("");
    var btns = [
      { t: "dark", n: "moon", l: "深色科技" },
      { t: "light", n: "sun", l: "彩色浅色" },
      { t: "mono", n: "contrast", l: "苹果极简" }
    ]
      .map(function (b) {
        return (
          '<button class="tsw-b" type="button" data-th="' + b.t + '" title="' + b.l +
          '" aria-label="' + b.l + '" aria-pressed="false">' + icon(b.n) + "</button>"
        );
      })
      .join("");
    return (
      '<header class="nav" id="nav"><div class="wrap nav-in">' +
      '<a class="brand" href="index.html">' + icon(S.brand.icon, "brand-i") +
      '<span class="b-tx">' + esc(S.brand.text) + "</span></a>" +
      '<nav class="nav-links" aria-label="版面导航">' + links + "</nav>" +
      '<div class="tsw" role="group" aria-label="配色皮肤">' + btns + "</div>" +
      "</div></header>"
    );
  }

  function footHTML() {
    var note = S.DEMO_MODE ? '<span class="demo-note">' + esc(S.demoNote) + "</span>" : "";
    return (
      '<footer class="foot"><div class="wrap foot-in">' +
      '<span class="foot-t">' + esc(S.brand.text) + "</span>" +
      '<div class="foot-l">' + note +
      '<a class="foot-a" href="#top">' + icon("arrow-up") + "回到顶部</a>" +
      "</div></div></footer>"
    );
  }

  function lightboxHTML() {
    return (
      '<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="查看系统界面原图">' +
      '<button class="lb-close" type="button" id="lb-close">' + icon("x") + "关闭</button>" +
      '<img id="lb-img" src="" alt="">' +
      '<div class="lb-tip">点击空白处或按 Esc 关闭</div>' +
      "</div>"
    );
  }

  /* ======================================================================
     四、首页渲染
     ====================================================================== */

  function capHTML(id, i) {
    var sc = S.scenarios[id];
    if (!sc) return "";
    return (
      '<a class="cap hero-l" style="--i:' + (i + 2) + '" href="' + esc(id) + '.html"' +
      ' data-cd="' + esc(sc.accent.d) + '" data-cl="' + esc(sc.accent.l) + '">' +
      '<span class="cap-n">' + esc(sc.nameEn) + "</span>" +
      '<span class="cap-b">' + icon(sc.icon) + "</span></a>"
    );
  }

  function cardHTML(id, i, big) {
    var sc = S.scenarios[id];
    if (!sc) return "";
    var hl = "";
    if (big && sc.values && sc.values.length) {
      hl =
        '<ul class="bhl">' +
        sc.values
          .slice(0, 3)
          .map(function (v) {
            return "<li>" + icon("check") + "<span>" + txt(v.k) + "</span></li>";
          })
          .join("") +
        "</ul>";
    }
    return (
      '<a class="bcard' + (big ? " bcard-a" : "") + ' rv" style="--i:' + i + '" href="' + esc(id) + '.html"' +
      ' data-cd="' + esc(sc.accent.d) + '" data-cl="' + esc(sc.accent.l) + '">' +
      '<div class="bcard-hd"><span class="tile">' + icon(sc.icon) + "</span>" +
      '<span class="mono">' + esc(sc.nameEn) + "</span></div>" +
      '<div class="bcard-bd"><h3 class="h3">' + txt(sc.name) + "</h3>" +
      '<p class="body">' + txt(sc.tagline) + "</p>" + hl + "</div>" +
      '<div class="bcard-ft"><span class="tlink">' + esc(U.viewScene) + icon("arrow-right") + "</span></div>" +
      "</a>"
    );
  }

  function chromaHTML(id, i) {
    var sc = S.scenarios[id];
    if (!sc) return "";
    return (
      '<a class="chroma rv" style="--i:' + i + '" href="' + esc(id) + '.html"' +
      ' data-cd="' + esc(sc.accent.d) + '" data-cl="' + esc(sc.accent.l) + '">' +
      '<svg class="chroma-wm" aria-hidden="true" focusable="false"><use href="#i-' + esc(sc.icon) + '"></use></svg>' +
      "<div><div class=\"mono mono-accent\">" + esc(sc.nameEn) + "</div>" +
      '<h3 class="h3" style="margin-top:12px">' + txt(sc.name) + "</h3></div>" +
      '<p class="body">' + txt(sc.tagline) + "</p>" +
      '<div class="chroma-ft"><span class="tlink">' + esc(U.viewScene) + icon("arrow-right") + "</span></div>" +
      "</a>"
    );
  }

  function renderHome() {
    var h = [];
    h.push('<section class="hero"><div class="wrap"><div class="hero-in">');
    h.push('<div class="hero-copy">');
    h.push('<h1 class="h1 hero-l" style="--i:0">' + esc(S.hero.h1a + S.hero.h1b) + "</h1>");
    h.push('<p class="lede hero-l" style="--i:1">' + esc(S.hero.lede) + "</p>");
    h.push('<div class="hero-cta hero-l" style="--i:2">');
    h.push('<a class="btn btn-p" href="' + esc(S.hero.primary.href) + '">' + esc(S.hero.primary.label) + icon("arrow-right") + "</a>");
    h.push('<a class="btn btn-g" href="' + esc(S.hero.secondary.href) + '">' + esc(S.hero.secondary.label) + "</a>");
    h.push("</div></div>");
    h.push('<div class="spectrum" aria-label="场景索引">');
    S.order.forEach(function (id, i) {
      h.push(capHTML(id, i));
    });
    h.push("</div>");
    h.push("</div></div></section>");

    S.sections.forEach(function (sec) {
      h.push('<section class="sec" id="' + esc(sec.id) + '" data-sec="' + esc(sec.id) + '"><div class="wrap">');
      h.push('<div class="sec-head rv">');
      h.push('<h2 class="h2">' + esc(sec.title) + "</h2>");
      h.push('<div class="sec-en">' + esc(sec.titleEn) + "</div>");
      h.push('<p class="body">' + txt(sec.desc) + "</p>");
      h.push("</div>");
      if (sec.layout === "bento") {
        h.push('<div class="bento">');
        sec.scenarios.forEach(function (id, i) {
          h.push(cardHTML(id, i, i === 0));
        });
        h.push("</div>");
      } else {
        h.push('<div class="chroma-grid">');
        sec.scenarios.forEach(function (id, i) {
          h.push(chromaHTML(id, i));
        });
        h.push("</div>");
      }
      h.push("</div></section>");
    });

    return h.join("");
  }

  /* ======================================================================
     五、详情页渲染
     ====================================================================== */

  function sectionOf(id) {
    for (var i = 0; i < S.sections.length; i++) {
      if (S.sections[i].scenarios.indexOf(id) >= 0) return S.sections[i];
    }
    return S.sections[0];
  }

  function neighbors(id) {
    var o = S.order;
    var i = o.indexOf(id);
    if (i < 0) return { prev: null, next: null };
    return {
      prev: i > 0 ? o[i - 1] : o[o.length - 1],
      next: i < o.length - 1 ? o[i + 1] : o[0]
    };
  }

  function blkHead(title, desc) {
    var h = '<div class="blk-head rv"><h2 class="h2">' + esc(title) + "</h2>";
    if (!isBlank(desc)) h += '<p class="body">' + esc(desc) + "</p>";
    return h + "</div>";
  }

  /* 首屏图片框（方案 B：横向框，图为主 + 细说明条） */
  function shotboxHTML(sc, sec) {
    if (!sc.screen || isBlank(sc.screen.overview)) return "";
    return (
      '<div><button class="shotbox hero-l" style="--i:2" type="button"' +
      ' data-lightbox="' + esc(sc.screen.overview) + '" data-cd="' + esc(sc.accent.d) +
      '" data-cl="' + esc(sc.accent.l) + '" aria-label="查看系统界面原图">' +
      '<span class="shot"><img src="' + esc(sc.screen.overview) + '" alt="' +
      esc(sc.screen.system) + ' 系统界面示意"></span>' +
      '<span class="shotcap"><span class="shotcap-main"><span class="shotname">' +
      txt(sc.screen.system) + '</span></span><span class="shotchip">' + esc(sec.title) +
      "</span></span></button>" +
      '<div class="shotnote">' + icon("search") + esc(U.clickHint) +
      " · 系统界面示意，数据为演示样例</div></div>"
    );
  }

  /* 决策人三问 */
  function qaHTML(sc) {
    if (!sc.qa || !sc.qa.length) return "";
    var items = sc.qa
      .map(function (x, i) {
        return (
          '<div class="qa rv" style="--i:' + i + '">' +
          '<div class="qa-q"><span class="qa-m">问</span>' +
          '<span class="qa-qt">' + txt(x.q) + "</span></div>" +
          '<div class="qa-a">' + txt(x.a) + "</div></div>"
        );
      })
      .join("");
    return (
      '<section class="blk"><div class="wrap">' +
      blkHead(U.qaTitle, U.qaDesc) +
      '<div class="qa-list">' + items + "</div></div></section>"
    );
  }

  /* 实施案例（仅 AI 财务场景） */
  function caseHTML(sc) {
    var c = sc.case;
    if (!c) return "";
    var claims = (c.claims || [])
      .map(function (x, i) {
        return (
          '<div class="case-claim rv" style="--i:' + i + '"><h3>' + txt(x.k) + "</h3>" +
          "<p>" + txt(x.v) + "</p></div>"
        );
      })
      .join("");
    var scale = (c.scale || [])
      .map(function (x) {
        return (
          '<div><div class="case-stat-k">' + esc(x.k) + "</div>" +
          '<div class="case-stat-v">' + esc(x.v) + "</div></div>"
        );
      })
      .join("");
    var rows = "";
    var lastG = null;
    (c.effort || []).forEach(function (x) {
      if (!isBlank(x.g) && x.g !== lastG) {
        rows += '<tr class="g"><td colspan="4">' + esc(x.g) + "</td></tr>";
        lastG = x.g;
      }
      rows +=
        "<tr><td>" + esc(x.k) + '</td><td class="num">' + esc(x.a) +
        '</td><td class="num">' + esc(x.b) + '</td><td class="num case-drop">' +
        pct(x.a, x.b) + "</td></tr>";
    });
    var total = c.effortTotal
      ? "<tr class=\"total\"><td>合计</td><td class=\"num\">" + esc(c.effortTotal.a) +
        '</td><td class="num">' + esc(c.effortTotal.b) + '</td><td class="num">' +
        pct(c.effortTotal.a, c.effortTotal.b) + "</td></tr>"
      : "";
    var miles = (c.milestones || [])
      .map(function (m) {
        return '<div class="case-mile">' + icon("check") + "<span>" + esc(m) + "</span></div>";
      })
      .join("");
    return (
      '<section class="blk band"><div class="wrap">' +
      '<div class="blk-head rv"><div class="mono" style="color:var(--accent);margin-bottom:14px">' +
      esc(U.caseLabel) + '</div><h2 class="h2">' + txt(c.title) + "</h2>" +
      '<p class="lede" style="margin-top:16px">' + txt(c.lede) + "</p></div>" +
      '<div class="case-claims">' + claims + "</div>" +
      '<div class="case-scale">' + scale + "</div>" +
      '<div class="case-effort rv">' +
      '<div class="case-effort-hd"><h3>月结投入对比</h3><span>单位：人天</span></div>' +
      "<table><thead><tr><th>环节</th><th class=\"num\" style=\"text-align:right\">手工</th>" +
      '<th class="num" style="text-align:right">系统</th>' +
      '<th class="num" style="text-align:right">降幅</th></tr></thead><tbody>' +
      rows + total + "</tbody></table></div>" +
      '<div class="case-miles">' + miles + "</div>" +
      '<div class="case-note rv">' + icon("alert-triangle") + "<span>" + esc(c.disclaimer) + "</span></div>" +
      "</div></section>"
    );
  }

  /* 明细大图（放在核心功能之前） */
  function figureHTML(sc) {
    if (!sc.screen || isBlank(sc.screen.detail)) return "";
    var head = blkHead(
      U.screenDetailLabel,
      isBlank(sc.screen.detailDesc) ? "" : sc.screen.detailDesc
    );
    return (
      '<section class="figure"><div class="wrap">' + head +
      '<button class="figure-wide rv" type="button" data-lightbox="' + esc(sc.screen.detail) +
      '" aria-label="查看界面明细原图">' +
      '<img src="' + esc(sc.screen.detail) + '" alt="' + esc(sc.screen.system) +
      ' 界面明细示意" loading="lazy"></button>' +
      '<div class="figurenote">' + esc(U.clickHint) + " · 系统界面示意，数据为演示样例</div>" +
      "</div></section>"
    );
  }

  function renderDetail() {
    var id = D.body.getAttribute("data-scenario");
    var sc = S.scenarios[id];
    if (!sc) {
      return '<div class="wrap" style="padding:120px 0"><h1 class="h2">未找到该场景</h1>' +
        '<p class="body" style="margin-top:12px">请检查文件名与 content.js 中的场景 id 是否一致。</p></div>';
    }
    var sec = sectionOf(id);
    var nb = neighbors(id);
    var h = [];

    /* ---- 首屏 ---- */
    h.push('<section class="dhero"><div class="wrap"><div class="dhero-in">');
    h.push('<div class="dhero-copy">');
    h.push('<a class="crumb hero-l" style="--i:0" href="index.html">' + icon("arrow-left") + esc(U.navHome) + "</a>");
    h.push('<div class="mono hero-l" style="--i:1">' + esc(sc.nameEn) + "</div>");
    h.push('<h1 class="h1 hero-l" style="--i:2">' + txt(sc.name) + "</h1>");
    h.push('<p class="lede hero-l" style="--i:3">' + txt(sc.tagline) + "</p>");
    h.push("</div>");
    h.push(shotboxHTML(sc, sec));
    h.push("</div>");

    /* 首屏下方的「打开首页能看到什么」 */
    if (sc.screen && !isBlank(sc.screen.overviewDesc)) {
      h.push('<div class="screendesc rv" data-cd="' + esc(sc.accent.d) + '" data-cl="' +
        esc(sc.accent.l) + '"><div class="lb2">' + esc(U.screenDescLabel) + "</div><p>" +
        txt(sc.screen.overviewDesc) + "</p></div>");
    }
    h.push("</div></section>");

    /* ---- 业务痛点 ---- */
    if (sc.pains && sc.pains.length) {
      h.push('<section class="blk tint"><div class="wrap">');
      h.push(blkHead(isBlank(sc.painTitle) ? U.painTitle : sc.painTitle, U.painDesc));
      h.push('<div class="pain-grid">');
      sc.pains.forEach(function (p, i) {
        h.push('<div class="pain rv" style="--i:' + i + '">');
        h.push('<span class="pain-i">' + icon("alert-triangle") + "</span>");
        h.push("<div><div class=\"pain-t\">" + txt(p.t) + '</div><div class="pain-d">' + txt(p.d) + "</div></div>");
        h.push("</div>");
      });
      h.push("</div></div></section>");
    }

    /* ---- 解决方案（全宽色带） ---- */
    if (sc.solution && sc.solution.length) {
      h.push('<section class="blk band"><div class="wrap">');
      h.push(blkHead(U.solTitle, U.solDesc));
      sc.solution.forEach(function (p) {
        h.push('<p class="sol-body rv">' + txt(p) + "</p>");
      });
      if (sc.techPoints && sc.techPoints.length) {
        h.push('<div class="chips rv">');
        sc.techPoints.forEach(function (t) {
          h.push('<span class="chip">' + icon("plug-connected") + txt(t) + "</span>");
        });
        h.push("</div>");
      }
      h.push("</div></section>");
    }

    /* ---- 客户价值 ---- */
    if (sc.values && sc.values.length) {
      h.push('<section class="blk"><div class="wrap">');
      h.push(blkHead(U.valTitle, U.valDesc));
      h.push('<div class="val-list">');
      sc.values.forEach(function (v, i) {
        h.push('<div class="val rv" style="--i:' + i + '">');
        h.push('<div class="val-k">' + txt(v.k) + "</div>");
        h.push('<div class="val-v">' + txt(v.v) + "</div>");
        h.push("</div>");
      });
      h.push("</div></div></section>");
    }

    /* ---- 决策人三问 ---- */
    h.push(qaHTML(sc));

    /* ---- 实施案例（仅 AI 财务） ---- */
    h.push(caseHTML(sc));

    /* ---- 界面明细大图 ---- */
    h.push(figureHTML(sc));

    /* ---- 核心功能 ---- */
    if (sc.features && sc.features.length) {
      h.push('<section class="blk tint"><div class="wrap">');
      h.push(blkHead(U.featTitle, U.featDesc));
      h.push('<div class="feat-grid">');
      sc.features.forEach(function (f, i) {
        h.push('<div class="feat rv" style="--i:' + i + '">');
        h.push('<span class="feat-i">' + icon("check") + "</span>");
        h.push('<div><div class="feat-t">' + txt(f.t) + '</div><div class="feat-d">' + txt(f.d) + "</div></div>");
        h.push("</div>");
      });
      h.push("</div></div></section>");
    }

    /* ---- 落地路径 ---- */
    if (sc.flow && sc.flow.length) {
      h.push('<section class="blk"><div class="wrap">');
      h.push(blkHead(U.flowTitle, U.flowDesc));
      h.push('<div class="flow">');
      sc.flow.forEach(function (s, i) {
        h.push('<div class="step rv" style="--i:' + i + '">');
        h.push('<span class="step-i">' + icon(i === sc.flow.length - 1 ? "check" : "arrow-narrow-right") + "</span>");
        h.push('<div class="step-t">' + txt(s.t) + '</div><div class="step-d">' + txt(s.d) + "</div>");
        h.push("</div>");
      });
      h.push("</div></div></section>");
    }

    /* ---- 适用对象 ---- */
    if (!isBlank(sc.audience)) {
      h.push('<section class="blk"><div class="wrap">');
      h.push('<div class="audience rv"><span class="aud-label">' + esc(U.audienceLabel) + "</span>" +
        '<span class="aud-text">' + txt(sc.audience) + "</span></div>");
      h.push("</div></section>");
    }

    /* ---- 页尾导航 ---- */
    h.push('<section class="pagenav"><div class="wrap">');
    h.push('<a class="crumb rv" href="index.html#' + esc(sec.id) + '">' + icon("arrow-left") +
      esc(U.navBackToSection) + "</a>");
    h.push('<div class="pn-grid" style="margin-top:20px">');
    if (nb.prev) {
      h.push('<a class="pn rv" style="--i:0" href="' + esc(nb.prev) + '.html"><span class="mono">' +
        esc(U.prev) + '</span><span class="pn-n">' + txt(S.scenarios[nb.prev].name) + "</span></a>");
    }
    if (nb.next) {
      h.push('<a class="pn pn-r rv" style="--i:1" href="' + esc(nb.next) + '.html"><span class="mono">' +
        esc(U.next) + '</span><span class="pn-n">' + txt(S.scenarios[nb.next].name) + "</span></a>");
    }
    h.push("</div></div></section>");

    return h.join("");
  }

  /* ======================================================================
     六、交互
     ====================================================================== */

  function initTheme() {
    var btns = D.querySelectorAll(".tsw-b");
    function sync() {
      var t = curTheme();
      for (var i = 0; i < btns.length; i++) {
        btns[i].setAttribute("aria-pressed", btns[i].getAttribute("data-th") === t ? "true" : "false");
      }
    }
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function () {
        var t = this.getAttribute("data-th");
        D.documentElement.setAttribute("data-theme", t);
        try { localStorage.setItem(TH_KEY, t); } catch (e) {}
        sync();
        applyColors();
      });
    }
    sync();
  }

  function initReveal() {
    var els = D.querySelectorAll(".rv");
    if (!els.length) return;
    function show(el) { el.classList.add("in"); }
    if (!("IntersectionObserver" in window)) {
      for (var j = 0; j < els.length; j++) show(els[j]);
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
        });
      },
      { rootMargin: "0px 0px 10% 0px", threshold: 0 }
    );
    for (var k = 0; k < els.length; k++) {
      var el = els[k];
      var r = el.getBoundingClientRect();
      if (r.top < (window.innerHeight || 0) || r.bottom <= 0) { show(el); continue; }
      io.observe(el);
    }
  }

  function initNavState() {
    var nav = D.getElementById("nav");
    if (!nav) return;
    var hero = D.querySelector(".hero, .dhero");
    if (hero && "IntersectionObserver" in window) {
      new IntersectionObserver(
        function (e) { nav.classList.toggle("solid", !e[0].isIntersecting); },
        { rootMargin: "-64px 0px 0px 0px", threshold: 0 }
      ).observe(hero);
    }
    var secs = D.querySelectorAll("[data-sec]");
    if (secs.length && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (e) {
            if (!e.isIntersecting) return;
            var id = e.target.getAttribute("data-sec");
            var links = D.querySelectorAll(".nav-a");
            for (var i = 0; i < links.length; i++) {
              links[i].classList.toggle("on", links[i].getAttribute("href").indexOf("#" + id) > -1);
            }
          });
        },
        { rootMargin: "-30% 0px -55% 0px", threshold: 0 }
      );
      for (var i = 0; i < secs.length; i++) io.observe(secs[i]);
    }
  }

  /* 图片灯箱 */
  function initLightbox() {
    var lb = D.getElementById("lb");
    var img = D.getElementById("lb-img");
    var close = D.getElementById("lb-close");
    if (!lb || !img) return;
    var lastFocus = null;

    function open(src, alt) {
      lastFocus = D.activeElement;
      img.setAttribute("src", src);
      img.setAttribute("alt", alt || "系统界面示意");
      lb.classList.add("on");
      D.documentElement.style.overflow = "hidden";
      close.focus();
    }
    function shut() {
      lb.classList.remove("on");
      img.setAttribute("src", "");
      D.documentElement.style.overflow = "";
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    var triggers = D.querySelectorAll("[data-lightbox]");
    for (var i = 0; i < triggers.length; i++) {
      triggers[i].addEventListener("click", function () {
        open(this.getAttribute("data-lightbox"), this.getAttribute("aria-label"));
      });
    }
    close.addEventListener("click", shut);
    lb.addEventListener("click", function (e) { if (e.target === lb) shut(); });
    D.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && lb.classList.contains("on")) shut();
    });
  }

  /* ======================================================================
     七、启动
     ====================================================================== */

  function boot() {
    var isDetail = D.body.hasAttribute("data-scenario");
    var activeId = null;

    if (isDetail) {
      var id = D.body.getAttribute("data-scenario");
      var sc = S.scenarios[id];
      if (sc) pageAccent = { d: sc.accent.d, l: sc.accent.l };
      activeId = sectionOf(id).id;
    }

    var mount = D.getElementById("app");
    mount.innerHTML =
      navHTML(activeId) +
      '<main id="top">' +
      (isDetail ? renderDetail() : renderHome()) +
      "</main>" +
      footHTML() +
      lightboxHTML();

    applyColors();
    initTheme();
    initReveal();
    initNavState();
    initLightbox();
  }

  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
