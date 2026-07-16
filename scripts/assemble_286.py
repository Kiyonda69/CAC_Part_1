#!/usr/bin/env python3
"""テンプレートと断片から 印刷286.html / 航大思考286.html を組み立てる"""
import os

SCRATCH = ("/tmp/claude-0/-home-user-CAC-Part-1/"
           "6d0896f3-0ade-5363-9dcf-99c69ea0c4a2/scratchpad")
FRAG = os.path.join(SCRATCH, "frag286")
SVG = os.path.join(SCRATCH, "svg286")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sub_svg(text):
    return (text.replace("{{SVG_Q1}}", read(os.path.join(SVG, "q1.svg")))
                .replace("{{SVG_Q2}}", read(os.path.join(SVG, "q2.svg"))))


def build_print():
    tpl = read("template_static.html")
    head = tpl[: tpl.index("<body>") + len("<body>\n")]
    js_marker = "    <!-- ==================== JavaScript ===================="
    tail = tpl[tpl.index(js_marker):]
    body = sub_svg(read(os.path.join(FRAG, "print_q1.html")) + "\n"
                   + read(os.path.join(FRAG, "print_q2.html")) + "\n")
    out = head + body + tail
    with open("印刷用/印刷286.html", "w", encoding="utf-8") as f:
        f.write(out)
    print("印刷用/印刷286.html:", len(out.splitlines()), "行")


def build_dynamic():
    tpl = read("template_dynamic.html")
    main_marker = '    <main class="main-content">\n'
    head = tpl[: tpl.index(main_marker) + len(main_marker)]
    progress = (
        "\n        <!-- ==================== プログレスバー ===================="
        " -->\n"
        '        <div class="progress-bar">\n'
        '            <div class="progress-dot" id="progress-1"'
        ' onclick="goToQuestion(1)">1</div>\n'
        '            <div class="progress-dot" id="progress-2"'
        ' onclick="goToQuestion(2)">2</div>\n'
        "        </div>\n\n"
    )
    tail = tpl[tpl.index("    </main>"):]
    tail = tail.replace("`2026_01/航大思考X/問${questionNum}`",
                        "`2026_07/航大思考286/問${questionNum}`")
    assert "航大思考286" in tail, "recordAnswer 置換失敗"
    body = sub_svg(read(os.path.join(FRAG, "dyn_q1.html")) + "\n"
                   + read(os.path.join(FRAG, "dyn_q2.html")) + "\n")
    out = head + progress + body + tail
    with open("航大思考問題/航大思考286.html", "w", encoding="utf-8") as f:
        f.write(out)
    print("航大思考問題/航大思考286.html:", len(out.splitlines()), "行")


if __name__ == "__main__":
    build_print()
    build_dynamic()
