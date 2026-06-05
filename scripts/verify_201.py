"""
航大思考201 検証スクリプト
資料解釈問題（航空関連）の解の一意性検証
"""


def verify_q1():
    """問1: 航空機の燃費改善に関する取り組み
    本文の事実と各選択肢の整合性をチェックする
    """
    # 本文から抽出した事実（fact = True で本文に明記）
    facts = {
        "1機あたりの燃料消費量を約15%削減": True,
        "総燃料消費量を15%削減": False,  # 「1機あたり」であり総ではない
        "総燃料消費量は微増": True,
        "総燃料消費量は減少": False,
        "新型機材の空気抵抗低減の理由は翼端形状の改良": True,
        "新型機材の空気抵抗低減の理由は座席数の増加": False,
        "ルート最適化で風向きと気温データの両方を活用": True,
        "ルート最適化で風向きのみを活用": False,
        "1機あたりと旅客一人あたりの両指標を併用": True,
    }

    options = {
        1: facts["総燃料消費量を15%削減"],
        2: facts["新型機材の空気抵抗低減の理由は座席数の増加"],
        3: facts["1機あたりと旅客一人あたりの両指標を併用"],
        4: facts["ルート最適化で風向きのみを活用"],
        5: facts["総燃料消費量は減少"],
    }

    correct = [k for k, v in options.items() if v]
    assert len(correct) == 1, f"問1の正解が{len(correct)}個（{correct}）"
    print(f"問1 正解: ({correct[0]})")
    return correct[0]


def verify_q2():
    """問2: 定時運航維持のための要因分析
    空港ごとの遅延主要因の対応関係をチェックする
    """
    # 本文に基づく事実テーブル
    # 各空港の遅延主要因
    airport_main_cause = {
        "X": "滑走路1本によるピーク時離着陸待機",
        "Y": "悪天候時の視界不良による出発便の地上待機",
        "Z": "駐機スポット不足による到着後の機材牽引待ち",
    }
    # 3年間の総遅延時間の推移
    delay_trend = {
        "X": "短縮",
        "Y": "大きな変化なし",
        "Z": "大きな変化なし",
    }
    # 地上ハンドリング効率化は根本的解消には至っていない
    handling_solves_root = False

    def check_option(text_claim):
        # 真偽を辞書ベースで判定
        return text_claim

    # 各選択肢の真偽
    options = {
        # (1) Y空港: 滑走路少ない、ピーク時離着陸待機が最多 → 偽
        1: (airport_main_cause["Y"] == "滑走路1本によるピーク時離着陸待機"),
        # (2) Z空港: 悪天候視界不良で出発便地上待機 → 偽
        2: (airport_main_cause["Z"] == "悪天候時の視界不良による出発便の地上待機"),
        # (3) 3空港すべてで総遅延時間が短縮 → 偽
        3: all(v == "短縮" for v in delay_trend.values()),
        # (4) 地上ハンドリング効率化が遅延の根本解消につながった → 偽
        4: handling_solves_root,
        # (5) Z空港: 駐機スポット不足による機材牽引待ちが中心 → 真
        5: (airport_main_cause["Z"] == "駐機スポット不足による到着後の機材牽引待ち"),
    }

    correct = [k for k, v in options.items() if v]
    assert len(correct) == 1, f"問2の正解が{len(correct)}個（{correct}）"
    print(f"問2 正解: ({correct[0]})")
    return correct[0]


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    assert q1 == 3, f"問1は(3)が正解のはず（実際: ({q1})）"
    assert q2 == 5, f"問2は(5)が正解のはず（実際: ({q2})）"
    print("\n検証完了: 解の一意性を確認")
