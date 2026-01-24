#!/usr/bin/env python3
"""
問題一覧.md 自動更新スクリプト

航大思考*.htmlファイルをスキャンし、問題一覧.mdを自動更新します。

使用方法:
    python3 scripts/update_index.py

機能:
    - HTMLファイルから問題情報を抽出
    - 問題一覧.mdを自動生成
    - 既存の分類情報がある場合は保持
"""

import os
import re
import glob
from datetime import date
from typing import Optional


def extract_problem_info(html_path: str) -> dict:
    """HTMLファイルから問題情報を抽出する"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {
        'filename': os.path.basename(html_path),
        'set_number': None,
        'q1_title': '',
        'q2_title': '',
        'q1_answer': None,
        'q2_answer': None,
    }

    # セット番号を抽出
    match = re.search(r'航大思考(\d+)\.html', html_path)
    if match:
        info['set_number'] = int(match.group(1))

    # 正解番号を抽出（問1）
    # 複数のフォーマットに対応: 問1(正解:(3)), 問1（正解: (2)）, 問1 (正解:(5))
    match = re.search(r'問1\s*[（(][^)）]*正解[：:]\s*\(?(\d)\)?', content)
    if match:
        info['q1_answer'] = int(match.group(1))

    # 正解番号を抽出（問2）
    match = re.search(r'問2\s*[（(][^)）]*正解[：:]\s*\(?(\d)\)?', content)
    if match:
        info['q2_answer'] = int(match.group(1))

    # 問題タイトル/概要を抽出（問1）
    # 「問1．」の後のテキストを取得
    match = re.search(r'問1[．.]\s*([^<]+)', content)
    if match:
        title = match.group(1).strip()
        # 長すぎる場合は短縮
        if len(title) > 50:
            title = title[:47] + '...'
        info['q1_title'] = title

    # 問題タイトル/概要を抽出（問2）
    match = re.search(r'問2[．.]\s*([^<]+)', content)
    if match:
        title = match.group(1).strip()
        if len(title) > 50:
            title = title[:47] + '...'
        info['q2_title'] = title

    return info


def load_existing_classifications(md_path: str) -> Optional[str]:
    """既存の問題一覧.mdから分類セクションを読み込む"""
    if not os.path.exists(md_path):
        return None

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 問題タイプ別分類セクションを抽出
    match = re.search(r'(## 問題タイプ別分類.*?)(?=## 統計|\Z)', content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return None


def generate_index_md(problems: list, classifications: Optional[str] = None) -> str:
    """問題一覧.mdの内容を生成する"""
    today = date.today().isoformat()

    lines = [
        "# 問題一覧",
        "",
        "航空大学校入学試験「総合Part I」思考パズル問題の一覧です。",
        "各ファイルには問1（標準難度）と問2（高難度）の2問が含まれています。",
        "",
        "## 作成済み問題セット",
        "",
        "| セット | ファイル名 | 問1 | 問2 |",
        "|:------:|-----------|-----|-----|",
    ]

    # 問題をセット番号順にソート
    problems.sort(key=lambda x: x['set_number'] if x['set_number'] else 999)

    for p in problems:
        set_num = p['set_number'] if p['set_number'] else '?'
        q1 = p['q1_title'] if p['q1_title'] else '（情報なし）'
        q2 = p['q2_title'] if p['q2_title'] else '（情報なし）'

        # タイトルが長すぎる場合は短縮表示
        if len(q1) > 40:
            q1 = q1[:37] + '...'
        if len(q2) > 40:
            q2 = q2[:37] + '...'

        lines.append(f"| {set_num} | {p['filename']} | {q1} | {q2} |")

    lines.append("")

    # 分類セクション
    if classifications:
        lines.append(classifications)
    else:
        lines.append("## 問題タイプ別分類")
        lines.append("")
        lines.append("（問題作成後に追記）")

    lines.append("")
    lines.append("## 統計")
    lines.append("")
    lines.append(f"- **総問題セット数**: {len(problems)}セット")
    lines.append(f"- **総問題数**: {len(problems) * 2}問（各セット2問）")
    lines.append(f"- **最終更新日**: {today}")
    lines.append("")

    return '\n'.join(lines)


def main():
    """メイン処理"""
    # プロジェクトルートを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # HTMLファイルを検索
    pattern = os.path.join(project_root, '航大思考*.html')
    html_files = glob.glob(pattern)

    if not html_files:
        print("警告: 航大思考*.html ファイルが見つかりませんでした")
        return

    print(f"検出されたHTMLファイル: {len(html_files)}件")

    # 各ファイルから情報を抽出
    problems = []
    for html_path in html_files:
        info = extract_problem_info(html_path)
        problems.append(info)
        print(f"  - {info['filename']}: 問1正解({info['q1_answer']}), 問2正解({info['q2_answer']})")

    # 既存の分類情報を読み込み
    md_path = os.path.join(project_root, '問題一覧.md')
    classifications = load_existing_classifications(md_path)

    # 問題一覧.mdを生成
    content = generate_index_md(problems, classifications)

    # ファイルに書き込み
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n問題一覧.md を更新しました")
    print(f"  - 総問題セット数: {len(problems)}")
    print(f"  - 総問題数: {len(problems) * 2}")


if __name__ == '__main__':
    main()
