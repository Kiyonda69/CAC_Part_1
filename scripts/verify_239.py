#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考239 検証コード: 姿勢指示器（人工水平儀）の読み取り

物理モデル:
- 姿勢指示器は「操縦席から見える実際の地平線」をそのまま表示する。
- 機体が左にバンク（左翼下がり）すると、パイロットの視界は機体と共に
  反時計回り（後方視点）に回転するため、地平線は逆方向（時計回り）に
  回転して見える → 計器の地平線は「左端が上・右端が下」。
- 機体が右にバンクすると逆 → 計器の地平線は「右端が上・左端が下」。
- 機首を上げると視線が上を向くため地平線は視界の下方へ移動
  → 計器の地平線は中央より下に表示される。機首下げなら上に表示。
- 地面（灰色）は常に地平線の下側。

表現:
- tilt: 'left_up'（左端上がり）/ 'right_up'（右端上がり）/ 'level'
- shift: 'down'（線が中央より下）/ 'up' / 'center'
- ground: 'below'（灰色が線の下側）/ 'above'
"""


def instrument_display(bank, pitch):
    """機体姿勢 (bank: 'left'/'right'/'none', pitch: 'up'/'down'/'none')
    から計器表示を導出する。"""
    if bank == 'left':
        tilt = 'left_up'    # 視界が左に回る→地平線は時計回り→左端上がり
    elif bank == 'right':
        tilt = 'right_up'   # 視界が右に回る→地平線は反時計回り→右端上がり
    else:
        tilt = 'level'
    if pitch == 'up':
        shift = 'down'      # 視線が上がる→地平線は下へ
    elif pitch == 'down':
        shift = 'up'
    else:
        shift = 'center'
    return (tilt, shift, 'below')  # 地面は必ず地平線の下側


def verify_q1():
    """問1: 真後ろから見て左翼が下がり30°傾いた機体（左バンク・水平飛行）。
    正しい計器表示は唯一か。"""
    expected = instrument_display('left', 'none')
    # 5つの選択肢 (tilt, shift, ground)
    options = {
        1: ('right_up', 'center', 'below'),  # 罠: 左右逆（鏡像エラー）
        2: ('left_up',  'center', 'above'),  # 罠: 傾き正・空地が逆
        3: ('level',    'center', 'below'),  # 罠: 傾きなし
        4: ('right_up', 'center', 'above'),  # 罠: 左右逆＋空地逆
        5: ('left_up',  'center', 'below'),  # 正解
    }
    matches = [n for n, disp in options.items() if disp == expected]
    assert len(matches) == 1, f"問1: 解が{len(matches)}個存在: {matches}"
    assert len(set(options.values())) == 5, "問1: 選択肢に重複あり"
    return matches[0]


def verify_q2():
    """問2: 右に30°バンク（後方視点で右翼下がり）＋機首上げ。
    正しい計器表示は唯一か。"""
    expected = instrument_display('right', 'up')
    options = {
        1: ('right_up', 'down',   'below'),  # 正解: 右端上がり・線は中央より下
        2: ('right_up', 'up',     'below'),  # 罠: ピッチ逆（線が上）
        3: ('left_up',  'down',   'below'),  # 罠: バンク逆（鏡像エラー）
        4: ('left_up',  'up',     'below'),  # 罠: 両方逆
        5: ('right_up', 'center', 'below'),  # 罠: ピッチ無視
    }
    matches = [n for n, disp in options.items() if disp == expected]
    assert len(matches) == 1, f"問2: 解が{len(matches)}個存在: {matches}"
    assert len(set(options.values())) == 5, "問2: 選択肢に重複あり"
    return matches[0]


def sanity_checks():
    """モデルの整合性確認（極端な場合で検算）"""
    # 左90°バンク: 地面はパイロットの左窓側に見える → 左端上がりで整合
    assert instrument_display('left', 'none')[0] == 'left_up'
    # 右バンクは左バンクの鏡像
    assert instrument_display('right', 'none')[0] == 'right_up'
    # 機首上げ→空が広く見える→地平線は下へ
    assert instrument_display('none', 'up')[1] == 'down'
    # 水平飛行→傾きなし・中央
    assert instrument_display('none', 'none') == ('level', 'center', 'below')


if __name__ == '__main__':
    sanity_checks()
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"問1: 唯一解を確認 → 正解 ({a1})")
    print(f"問2: 唯一解を確認 → 正解 ({a2})")
