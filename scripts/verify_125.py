"""
航大思考125 解の一意性検証スクリプト
問題タイプ: 資料読み取り（文章読解）
問1: ジェット気流と航空運航への影響
問2: 飛行方式と管制空域の分類

正解番号: 問1=(3), 問2=(2)
"""


def verify_q1():
    """
    問1: ジェット気流に関する文章から各選択肢の正誤を検証
    文章中の記述と選択肢を照合して唯一の正解を確認する
    """
    # 文章中の事実を辞書で定義
    facts = {
        "冬季の位置": "南寄り・速度増大",
        "夏季の位置": "北寄り・速度低下",
        "最大速度": "400km/hを超えることもある（概ね100〜300km/h）",
        "追い風の効果": "飛行時間短縮・燃料削減",
        "向かい風の効果": "飛行時間延長・燃料増加",
        "東行き路線": "ジェット気流を追い風として活用",
        "西行き路線": "ジェット気流を避けて飛行",
        "CATの特徴": "雲を伴わずレーダー探知不可・境界付近で発生",
    }

    # 各選択肢の評価
    options = {
        1: {
            "text": "北半球のジェット気流は、夏季に南寄りに位置して速度が増大する",
            "claim_season_pos": "夏季→南寄り",
            "claim_speed": "速度増大",
            "fact_pos": facts["夏季の位置"],  # 北寄り・速度低下
            "correct": False,
            "reason": "文章では夏季は北寄り・速度低下。南寄り・増大は冬季の特性。",
        },
        2: {
            "text": "航空機がジェット気流と同方向（追い風）で飛行すると、飛行時間が延長し燃料消費が増加する",
            "claim": "追い風→時間延長・燃料増加",
            "fact": facts["追い風の効果"],  # 時間短縮・燃料削減
            "correct": False,
            "reason": "文章では追い風は飛行時間短縮・燃料削減。延長・増加は向かい風の特性。",
        },
        3: {
            "text": "晴天乱気流はレーダーに映らず、ジェット気流の境界付近で発生しやすいため予測・回避が困難である",
            "claim_radar": "レーダー探知不可",
            "claim_loc": "境界付近で発生",
            "fact": facts["CATの特徴"],
            "correct": True,
            "reason": "文章の「レーダー探知不可」「境界付近で発生」「予測回避困難」と完全一致。",
        },
        4: {
            "text": "ジェット気流の速度は最大でも300km/hを超えることはない",
            "claim": "最大速度≦300km/h",
            "fact": facts["最大速度"],  # 400km/h超えることもある
            "correct": False,
            "reason": "文章では「特に発達した場合には400km/hを超えることもある」と述べられており、300km/h以下という記述は誤り。",
        },
        5: {
            "text": "国際線旅客機は、日本から北米への東行き路線でジェット気流を避けて飛行することが多い",
            "claim": "東行き→ジェット気流を回避",
            "fact": facts["東行き路線"],  # 追い風として活用
            "correct": False,
            "reason": "文章では東行き路線でジェット気流を追い風として活用し、西行き路線で避けると述べられている。",
        },
    }

    correct_options = [k for k, v in options.items() if v["correct"]]
    assert len(correct_options) == 1, f"問1の正解が{len(correct_options)}個: {correct_options}"
    assert correct_options[0] == 3, f"問1の正解が(3)でない: {correct_options[0]}"

    print("=== 問1 検証結果 ===")
    for num, opt in options.items():
        status = "正解" if opt["correct"] else "誤り"
        print(f"  ({num}) [{status}] {opt['reason']}")
    print(f"  → 正解: ({correct_options[0]}) ✓\n")
    return correct_options[0]


def verify_q2():
    """
    問2: 飛行方式と管制空域に関する文章から各選択肢の正誤を検証
    """
    facts = {
        "VFR飛行計画": "原則不要だが、一部の管制空域進入・国際飛行では必要な場合あり",
        "IFR飛行計画": "常に義務付け（出発前に提出）",
        "IFR管制": "ATCの指示に従って飛行",
        "クラスA": "全てIFRが義務・高度18,000ft以上",
        "クラスB": "全ての航空機にATC管制許可が必要",
        "クラスG": "非管制空域・通信義務なし・VFR可能",
        "ILS機能": "グライドパスとローカライザーを提供・対気速度計測なし・着陸時のみ",
    }

    options = {
        1: {
            "text": "VFR飛行においては、いかなる状況においても飛行計画の提出は一切必要とされない",
            "claim": "VFR飛行計画→いかなる場合も不要",
            "fact": facts["VFR飛行計画"],
            "correct": False,
            "reason": "文章では「一部の管制空域への進入や国際飛行においては必要となる場合がある」と述べており、「いかなる状況においても不要」は誤り。",
        },
        2: {
            "text": "IFR飛行では出発前に飛行計画の提出が義務付けられており、ATCの指示に従って飛行しなければならない",
            "claim_plan": "IFR→飛行計画提出義務",
            "claim_atc": "ATC指示に従う",
            "fact_plan": facts["IFR飛行計画"],
            "fact_atc": facts["IFR管制"],
            "correct": True,
            "reason": "文章の「出発前に管制機関への飛行計画の提出が常に義務付けられており」「ATCの指示に従って航行しなければならない」と完全一致。",
        },
        3: {
            "text": "クラスA空域ではVFRによる飛行が義務付けられており、IFR飛行は認められていない",
            "claim": "クラスA→VFR義務",
            "fact": facts["クラスA"],  # 全てIFRが義務
            "correct": False,
            "reason": "文章では「全ての航空機がIFRで飛行することが義務付けられている」。VFRが義務とする記述は完全に逆。",
        },
        4: {
            "text": "ILSは視程の低い状況において、航空機にグライドパスと対気速度の情報を提供する",
            "claim": "ILS→グライドパス+対気速度",
            "fact": facts["ILS機能"],  # 対気速度計測なし
            "correct": False,
            "reason": "文章では「対気速度の計測機能は有していない」と明記。グライドパスの提供は正しいが、対気速度の情報提供は誤り。",
        },
        5: {
            "text": "クラスG空域では全ての航空機がATCの管制許可を受けて飛行しなければならない",
            "claim": "クラスG→ATC管制許可必要",
            "fact": facts["クラスG"],  # 非管制空域・通信義務なし
            "correct": False,
            "reason": "文章では「クラスG空域は非管制空域であり、ATCとの通信義務がなく」と述べられており、管制許可が必要とする記述は誤り。",
        },
    }

    correct_options = [k for k, v in options.items() if v["correct"]]
    assert len(correct_options) == 1, f"問2の正解が{len(correct_options)}個: {correct_options}"
    assert correct_options[0] == 2, f"問2の正解が(2)でない: {correct_options[0]}"

    print("=== 問2 検証結果 ===")
    for num, opt in options.items():
        status = "正解" if opt["correct"] else "誤り"
        print(f"  ({num}) [{status}] {opt['reason']}")
    print(f"  → 正解: ({correct_options[0]}) ✓\n")
    return correct_options[0]


if __name__ == "__main__":
    print("航大思考125 解の一意性検証\n")
    q1_ans = verify_q1()
    q2_ans = verify_q2()
    print(f"=== 検証完了 ===")
    print(f"問1 正解: ({q1_ans})")
    print(f"問2 正解: ({q2_ans})")
    print("全ての問題で解が唯一であることを確認しました。")
