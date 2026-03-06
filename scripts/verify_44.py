#!/usr/bin/env python3
"""
航大思考44 - 検証スクリプト
問1: 散布図（蔵書数と貸出冊数の推移）から合計が減少した年を特定
問2: 空港利用客の表から出張客数・観光客数を逆算し、出張客が上回る地域の出張客合計を求める
"""

def verify_q1():
    """問1: 蔵書数と貸出冊数の合計が前回比で減少した年を特定"""
    # データ: (年, 蔵書数(万冊), 貸出冊数(万冊))
    data = [
        (1990, 80, 180),
        (1995, 105, 230),
        (2000, 130, 280),
        (2005, 155, 250),
        (2010, 180, 300),
        (2015, 210, 340),
        (2020, 240, 370),
    ]
    
    totals = [(y, b+l) for y, b, l in data]
    print("=== 問1 検証 ===")
    print("年度ごとの合計と前回比:")
    
    decreased_years = []
    for i, (year, total) in enumerate(totals):
        if i == 0:
            print(f"  {year}年: 蔵書{data[i][1]} + 貸出{data[i][2]} = {total}")
        else:
            diff = total - totals[i-1][1]
            status = "減少" if diff < 0 else "増加"
            print(f"  {year}年: 蔵書{data[i][1]} + 貸出{data[i][2]} = {total} (前回比: {diff:+d}, {status})")
            if diff < 0:
                decreased_years.append(year)
    
    print(f"\n減少した年: {decreased_years}")
    assert len(decreased_years) == 1, f"減少した年が{len(decreased_years)}個: {decreased_years}"
    assert decreased_years[0] == 2005, f"期待: 2005, 実際: {decreased_years[0]}"
    print(f"正解: {decreased_years[0]}年")
    return decreased_years[0]


def verify_q2():
    """問2: 空港利用客のデータから出張客が観光客を上回る地域の出張客合計を求める"""
    total_passengers = 4500
    
    # 割合（%）
    business_pct = {'北米': 40.0, 'ヨーロッパ': 20.0, 'アジア': 25.0, 'オセアニア': 8.0, 'その他': 7.0}
    leisure_pct = {'北米': 20.0, 'ヨーロッパ': 35.0, 'アジア': 15.0, 'オセアニア': 18.0, 'その他': 12.0}
    overall_pct = {'北米': 28.0, 'ヨーロッパ': 29.0, 'アジア': 19.0, 'オセアニア': 14.0, 'その他': 10.0}
    
    # 各行の合計が100%か確認
    assert abs(sum(business_pct.values()) - 100.0) < 0.01, f"出張合計: {sum(business_pct.values())}"
    assert abs(sum(leisure_pct.values()) - 100.0) < 0.01, f"観光合計: {sum(leisure_pct.values())}"
    assert abs(sum(overall_pct.values()) - 100.0) < 0.01, f"全体合計: {sum(overall_pct.values())}"
    
    # 出張客数Bを連立方程式で求める
    # 北米: 0.40B + 0.20(4500-B) = 0.28 * 4500
    # 0.40B + 900 - 0.20B = 1260
    # 0.20B = 360
    # B = 1800
    B = (overall_pct['北米']/100 * total_passengers - leisure_pct['北米']/100 * total_passengers) / (business_pct['北米']/100 - leisure_pct['北米']/100)
    L = total_passengers - B
    
    print("\n=== 問2 検証 ===")
    print(f"出張客: {B:.0f}人, 観光客: {L:.0f}人")
    
    # 整合性チェック: すべての地域で全体の割合と一致するか
    for region in business_pct:
        computed = (business_pct[region]/100 * B + leisure_pct[region]/100 * L) / total_passengers * 100
        expected = overall_pct[region]
        assert abs(computed - expected) < 0.01, f"{region}: 計算値{computed:.1f}% != 期待値{expected:.1f}%"
        print(f"  {region}: 出張{business_pct[region]/100*B:.0f} + 観光{leisure_pct[region]/100*L:.0f} = {business_pct[region]/100*B + leisure_pct[region]/100*L:.0f} ({computed:.1f}%)")
    
    # 出張客が観光客を上回る地域を特定
    print(f"\n地域別比較:")
    surplus_regions = []
    surplus_business_total = 0
    for region in business_pct:
        biz = business_pct[region]/100 * B
        lei = leisure_pct[region]/100 * L
        if biz > lei:
            surplus_regions.append(region)
            surplus_business_total += biz
            print(f"  {region}: 出張{biz:.0f} > 観光{lei:.0f} → 出張が上回る")
        else:
            print(f"  {region}: 出張{biz:.0f} <= 観光{lei:.0f}")
    
    print(f"\n出張が上回る地域: {surplus_regions}")
    print(f"それらの地域の出張客合計: {surplus_business_total:.0f}人")
    
    assert abs(surplus_business_total - 1170) < 0.01, f"期待: 1170, 実際: {surplus_business_total:.0f}"
    return int(surplus_business_total)


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    print(f"\n=== 最終結果 ===")
    print(f"問1正解: {q1_answer}年")
    print(f"問2正解: {q2_answer}人")
    print("検証完了: すべてのテストに合格")
