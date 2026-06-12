#!/usr/bin/env python3
"""航大思考213 のHTMLファイルをテンプレート＋本文＋SVGスニペットから組み立てる"""
import re

SNIPPET_DIR = "/tmp/svg213"
JS_MARKER = "    <!-- ==================== JavaScript ==================== -->"


def load(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def substitute_svg(text):
    """<!--SVG:name--> マーカーをスニペット内容（インデント付き）に置換"""
    def repl(m):
        name = m.group(1)
        svg = load(f"{SNIPPET_DIR}/{name}.svg")
        indent = " " * 24
        return "\n".join(indent + line for line in svg.split("\n"))
    return re.sub(r"<!--SVG:(\w+)-->", repl, text)


def splice_body(template_text, body_text):
    """<body> と JavaScriptコメントの間を新しい本文に差し替える"""
    start = template_text.index("<body>") + len("<body>")
    end = template_text.index(JS_MARKER)
    return template_text[:start] + "\n" + body_text + "\n\n" + template_text[end:]


def build_static():
    tpl = load("template_static.html")
    body = substitute_svg(load(f"{SNIPPET_DIR}/body_static.html"))
    out = splice_body(tpl, body)
    with open("印刷用/印刷213.html", "w", encoding="utf-8") as fp:
        fp.write(out)
    print(f"印刷用/印刷213.html: {len(out)} bytes")


def build_dynamic():
    tpl = load("template_dynamic.html")
    body = substitute_svg(load(f"{SNIPPET_DIR}/body_dynamic.html"))
    out = splice_body(tpl, body)
    out = out.replace("2026_01/航大思考X", "2026_06/航大思考213")
    assert "2026_06/航大思考213" in out, "recordAnswer の問題名置換に失敗"
    with open("航大思考問題/航大思考213.html", "w", encoding="utf-8") as fp:
        fp.write(out)
    print(f"航大思考問題/航大思考213.html: {len(out)} bytes")


if __name__ == "__main__":
    build_static()
    build_dynamic()
