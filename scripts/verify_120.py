"""
航大思考120 解答検証スクリプト

問1（標準）: 図書館4館 × 3カテゴリ（小説/専門書/児童書）の貸出統計
問2（高難度）: 研修施設4会議室 × 3カ月（4-6月）× 3指標（件数/時間/収益）の利用統計

各空欄の値を計算し、選択肢の中で全条件を満たすものが唯一であることを検証する。
"""

# ============================================================
# 問1: 図書館貸出データ
# ============================================================

library_data = {
    "A": {"小説": 800, "専門書": 400, "児童書": 300},
    "B": {"小説": 500, "専門書": 300, "児童書": 600},
    "C": {"小説": 400, "専門書": 500, "児童書": 300},
    "D": {"小説": 800, "専門書": 300, "児童書": 700},
}

# ア: 4館合計の小説貸出冊数
total_novels = sum(d["小説"] for d in library_data.values())

# イ: 児童書比率（児童書÷各館合計）が最も高い館
child_ratios = {k: v["児童書"] / sum(v.values()) for k, v in library_data.items()}
max_ratio_lib = max(child_ratios, key=child_ratios.get)

# ウ: 専門書冊数 > 小説冊数 となる館の数
spec_over_novel = sum(1 for v in library_data.values() if v["専門書"] > v["小説"])

# エ: 全館全カテゴリの貸出冊数の合計
grand_total = sum(sum(v.values()) for v in library_data.values())

print("===== 問1 各空欄の正解 =====")
print(f"ア (4館合計の小説冊数): {total_novels}")
print(f"イ (児童書比率最大の館): {max_ratio_lib}  比率={child_ratios}")
print(f"ウ (専門書>小説の館数): {spec_over_novel}")
print(f"エ (全館合計貸出冊数): {grand_total}")

# 児童書合計（ひっかけ用に確認）
child_total = sum(d["児童書"] for d in library_data.values())
print(f"  参考: 児童書合計={child_total}")

q1_options = {
    1: {"ア": 2500, "イ": "D", "ウ": 1, "エ": 5900},
    2: {"ア": 2500, "イ": "B", "ウ": 2, "エ": 5900},
    3: {"ア": 1900, "イ": "B", "ウ": 1, "エ": 5900},
    4: {"ア": 2500, "イ": "B", "ウ": 1, "エ": 1900},
    5: {"ア": 2500, "イ": "B", "ウ": 1, "エ": 5900},
}
correct_q1 = {"ア": total_novels, "イ": max_ratio_lib, "ウ": spec_over_novel, "エ": grand_total}
matches_q1 = [k for k, v in q1_options.items() if v == correct_q1]
assert matches_q1 == [5], f"問1の解が一意でない: {matches_q1}"
print(f"問1 正解: ({matches_q1[0]})  ←一意性OK\n")


# ============================================================
# 問2: 研修施設 会議室利用データ
# ============================================================
# 月間総開館時間 = 180h（30日 × 6h）。3カ月で540h。

months = ["4月", "5月", "6月"]
rooms = {
    "α": {
        "4月": {"件数": 20, "時間": 60,  "収益": 150},
        "5月": {"件数": 25, "時間": 80,  "収益": 200},
        "6月": {"件数": 30, "時間": 100, "収益": 250},
    },
    "β": {
        "4月": {"件数": 15, "時間": 90,  "収益": 270},
        "5月": {"件数": 18, "時間": 100, "収益": 300},
        "6月": {"件数": 20, "時間": 120, "収益": 360},
    },
    "γ": {
        "4月": {"件数": 10, "時間": 80,  "収益": 320},
        "5月": {"件数": 12, "時間": 100, "収益": 400},
        "6月": {"件数": 14, "時間": 120, "収益": 480},
    },
    "δ": {
        "4月": {"件数": 4,  "時間": 60,  "収益": 270},
        "5月": {"件数": 5,  "時間": 80,  "収益": 360},
        "6月": {"件数": 6,  "時間": 100, "収益": 450},
    },
}
MONTHLY_OPEN_H = 180
TOTAL_OPEN_H = MONTHLY_OPEN_H * 3  # 540

# ア: 4室合計の利用時間（4-6月3カ月分）
total_hours = sum(rooms[r][m]["時間"] for r in rooms for m in months)

# イ: 6月の時間あたり収益（収益÷時間）が最も高い会議室
june_rate = {r: rooms[r]["6月"]["収益"] / rooms[r]["6月"]["時間"] for r in rooms}
best_june_rate = max(june_rate, key=june_rate.get)

# ウ: 各室の3カ月平均利用率（時間合計÷540）が50%以上の会議室の数
util_ratio = {r: sum(rooms[r][m]["時間"] for m in months) / TOTAL_OPEN_H for r in rooms}
util_over50 = sum(1 for v in util_ratio.values() if v >= 0.50)

# エ: γ室の3カ月平均月間収益（千円）
gamma_avg = sum(rooms["γ"][m]["収益"] for m in months) / 3

# オ: 4室全体の3カ月の収益合計（千円）
total_revenue = sum(rooms[r][m]["収益"] for r in rooms for m in months)

print("===== 問2 各空欄の正解 =====")
print(f"ア (3カ月の利用時間合計): {total_hours} h")
print(f"イ (6月の時間あたり収益最大の室): {best_june_rate}  rate={june_rate}")
print(f"ウ (利用率50%以上の会議室数): {util_over50}  ratios={ {k: round(v*100,1) for k,v in util_ratio.items()} }")
print(f"エ (γ室の3カ月平均月間収益): {gamma_avg} 千円")
print(f"オ (4室全体の3カ月収益合計): {total_revenue} 千円")

# 件数合計（ひっかけ用に確認）
total_count = sum(rooms[r][m]["件数"] for r in rooms for m in months)
print(f"  参考: 件数合計={total_count}")
# γ3カ月合計収益（ひっかけ）
gamma_sum = sum(rooms["γ"][m]["収益"] for m in months)
print(f"  参考: γ3カ月合計収益={gamma_sum}")
# 各室3カ月収益合計
for r in rooms:
    print(f"  参考: {r}室3カ月収益合計={sum(rooms[r][m]['収益'] for m in months)}")

q2_options = {
    1: {"ア": 1090, "イ": "δ", "ウ": 2, "エ": 400,  "オ": 3810},
    2: {"ア": 1090, "イ": "γ", "ウ": 2, "エ": 400,  "オ": 3810},
    3: {"ア": 1090, "イ": "δ", "ウ": 3, "エ": 400,  "オ": 3810},
    4: {"ア": 1090, "イ": "δ", "ウ": 2, "エ": 1200, "オ": 3810},
    5: {"ア": 179,  "イ": "δ", "ウ": 2, "エ": 400,  "オ": 3810},
}
correct_q2 = {
    "ア": int(total_hours),
    "イ": best_june_rate,
    "ウ": util_over50,
    "エ": int(gamma_avg),
    "オ": int(total_revenue),
}
matches_q2 = [k for k, v in q2_options.items() if v == correct_q2]
assert matches_q2 == [1], f"問2の解が一意でない: {matches_q2}"
print(f"\n問2 正解: ({matches_q2[0]})  ←一意性OK")
