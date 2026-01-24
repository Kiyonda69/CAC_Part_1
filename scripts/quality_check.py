#!/usr/bin/env python3
"""
品質チェックスクリプト

航大思考*.htmlファイルの品質をチェックします。

使用方法:
    python3 scripts/quality_check.py              # 全ファイルをチェック
    python3 scripts/quality_check.py 航大思考1.html  # 特定ファイルをチェック

チェック項目:
    - viewBox属性の有無
    - SVGサイズが推奨範囲内か
    - 正解番号の分布（偏りがないか）
    - 解説セクションの有無
    - 問題番号の整合性
"""

import os
import re
import sys
import glob
from collections import Counter
from typing import Optional


class QualityChecker:
    """HTMLファイルの品質チェッカー"""

    # 推奨SVGサイズ
    MAX_SVG_WIDTH = 650
    MAX_SVG_HEIGHT = 500

    def __init__(self, html_path: str):
        self.path = html_path
        self.filename = os.path.basename(html_path)
        self.errors = []
        self.warnings = []
        self.info = []

        with open(html_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def check_all(self) -> bool:
        """全てのチェックを実行"""
        self.check_viewbox()
        self.check_svg_sizes()
        self.check_answers()
        self.check_explanations()
        self.check_problem_structure()
        return len(self.errors) == 0

    def check_viewbox(self):
        """SVGにviewBox属性があるかチェック"""
        # 全てのSVGタグを抽出
        svg_pattern = r'<svg[^>]*>'
        svg_tags = re.findall(svg_pattern, self.content, re.IGNORECASE)

        if not svg_tags:
            self.info.append("SVGタグが見つかりませんでした")
            return

        for i, tag in enumerate(svg_tags, 1):
            if 'viewBox' not in tag and 'viewbox' not in tag:
                self.errors.append(f"SVG #{i}: viewBox属性がありません")
            else:
                self.info.append(f"SVG #{i}: viewBox OK")

    def check_svg_sizes(self):
        """SVGサイズが推奨範囲内かチェック"""
        svg_pattern = r'<svg[^>]*width=["\'](\d+)["\'][^>]*height=["\'](\d+)["\'][^>]*>'
        matches = re.findall(svg_pattern, self.content, re.IGNORECASE)

        # 逆順のパターンも確認
        svg_pattern2 = r'<svg[^>]*height=["\'](\d+)["\'][^>]*width=["\'](\d+)["\'][^>]*>'
        matches2 = re.findall(svg_pattern2, self.content, re.IGNORECASE)
        matches2 = [(w, h) for h, w in matches2]  # 順序を揃える

        all_matches = matches + matches2

        for i, (width, height) in enumerate(all_matches, 1):
            w, h = int(width), int(height)

            if w > self.MAX_SVG_WIDTH:
                self.warnings.append(
                    f"SVG #{i}: 幅 {w}px が推奨値 {self.MAX_SVG_WIDTH}px を超えています"
                )
            if h > self.MAX_SVG_HEIGHT:
                self.warnings.append(
                    f"SVG #{i}: 高さ {h}px が推奨値 {self.MAX_SVG_HEIGHT}px を超えています"
                )

    def check_answers(self) -> tuple:
        """正解番号を抽出"""
        q1_answer = None
        q2_answer = None

        # 複数のフォーマットに対応: 問1(正解:(3)), 問1（正解: (2)）, 問1 (正解:(5))
        match = re.search(r'問1\s*[（(][^)）]*正解[：:]\s*\(?(\d)\)?', self.content)
        if match:
            q1_answer = int(match.group(1))
        else:
            self.warnings.append("問1の正解番号が見つかりません")

        match = re.search(r'問2\s*[（(][^)）]*正解[：:]\s*\(?(\d)\)?', self.content)
        if match:
            q2_answer = int(match.group(1))
        else:
            self.warnings.append("問2の正解番号が見つかりません")

        return q1_answer, q2_answer

    def check_explanations(self):
        """解説セクションの有無をチェック"""
        # 複数のフォーマットに対応
        q1_explanation = (
            '問1の解説' in self.content or
            '問1(正解' in self.content or
            '問1（正解' in self.content or
            '問1 (正解' in self.content
        )
        if not q1_explanation:
            self.warnings.append("問1の解説セクションが見つかりません")

        q2_explanation = (
            '問2の解説' in self.content or
            '問2(正解' in self.content or
            '問2（正解' in self.content or
            '問2 (正解' in self.content
        )
        if not q2_explanation:
            self.warnings.append("問2の解説セクションが見つかりません")

    def check_problem_structure(self):
        """問題構造の整合性をチェック"""
        # 問1と問2が存在するか
        if '問1' not in self.content:
            self.errors.append("問1が見つかりません")
        if '問2' not in self.content:
            self.errors.append("問2が見つかりません")

        # 選択肢(1)〜(5)が存在するか
        for i in range(1, 6):
            pattern = rf'\({i}\)'
            if not re.search(pattern, self.content):
                self.warnings.append(f"選択肢({i})が見つかりません")

    def print_report(self):
        """チェック結果を表示"""
        print(f"\n{'='*60}")
        print(f"ファイル: {self.filename}")
        print('='*60)

        if self.errors:
            print("\n[エラー]")
            for e in self.errors:
                print(f"  X {e}")

        if self.warnings:
            print("\n[警告]")
            for w in self.warnings:
                print(f"  ! {w}")

        if self.info:
            print("\n[情報]")
            for i in self.info:
                print(f"  - {i}")

        if not self.errors and not self.warnings:
            print("\n  全てのチェックをパスしました")


def check_answer_distribution(all_answers: list):
    """正解番号の分布をチェック"""
    print("\n" + "="*60)
    print("正解番号の分布")
    print("="*60)

    q1_answers = [a[0] for a in all_answers if a[0] is not None]
    q2_answers = [a[1] for a in all_answers if a[1] is not None]
    all_combined = q1_answers + q2_answers

    print("\n[問1の正解番号分布]")
    q1_counter = Counter(q1_answers)
    for i in range(1, 6):
        count = q1_counter.get(i, 0)
        bar = '#' * count
        print(f"  ({i}): {bar} ({count})")

    print("\n[問2の正解番号分布]")
    q2_counter = Counter(q2_answers)
    for i in range(1, 6):
        count = q2_counter.get(i, 0)
        bar = '#' * count
        print(f"  ({i}): {bar} ({count})")

    print("\n[全体の正解番号分布]")
    total_counter = Counter(all_combined)
    for i in range(1, 6):
        count = total_counter.get(i, 0)
        bar = '#' * count
        print(f"  ({i}): {bar} ({count})")

    # 偏りチェック
    if all_combined:
        avg = len(all_combined) / 5
        for i in range(1, 6):
            count = total_counter.get(i, 0)
            if count == 0:
                print(f"\n  警告: 正解番号({i})が一度も使用されていません")
            elif count > avg * 1.5:
                print(f"\n  警告: 正解番号({i})が多すぎる可能性があります ({count}回)")
            elif count < avg * 0.5 and count > 0:
                print(f"\n  警告: 正解番号({i})が少なすぎる可能性があります ({count}回)")


def main():
    """メイン処理"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # 引数でファイル指定があれば特定ファイルのみ
    if len(sys.argv) > 1:
        files_to_check = []
        for arg in sys.argv[1:]:
            if os.path.isabs(arg):
                files_to_check.append(arg)
            else:
                files_to_check.append(os.path.join(project_root, arg))
    else:
        pattern = os.path.join(project_root, '航大思考*.html')
        files_to_check = sorted(glob.glob(pattern))

    if not files_to_check:
        print("チェック対象のファイルが見つかりません")
        return 1

    print(f"チェック対象: {len(files_to_check)}ファイル")

    all_answers = []
    total_errors = 0
    total_warnings = 0

    for html_path in files_to_check:
        if not os.path.exists(html_path):
            print(f"ファイルが見つかりません: {html_path}")
            continue

        checker = QualityChecker(html_path)
        checker.check_all()
        checker.print_report()

        total_errors += len(checker.errors)
        total_warnings += len(checker.warnings)

        answers = checker.check_answers()
        all_answers.append(answers)

    # 複数ファイルの場合は分布チェック
    if len(files_to_check) > 1:
        check_answer_distribution(all_answers)

    # サマリー
    print("\n" + "="*60)
    print("サマリー")
    print("="*60)
    print(f"  チェックファイル数: {len(files_to_check)}")
    print(f"  エラー総数: {total_errors}")
    print(f"  警告総数: {total_warnings}")

    if total_errors > 0:
        print("\n  結果: エラーがあります。修正してください。")
        return 1
    elif total_warnings > 0:
        print("\n  結果: 警告があります。確認を推奨します。")
        return 0
    else:
        print("\n  結果: 全てのチェックをパスしました。")
        return 0


if __name__ == '__main__':
    sys.exit(main())
