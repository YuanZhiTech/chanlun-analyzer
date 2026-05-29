     1|"""
     2|K线包含处理模块 — 单元测试
     3|"""
     4|
     5|import pytest
     6|from chanlun.kline import merge_kline_bars, is_containing
     7|
     8|
     9|def make_bar(high, low, open_=None, close=None):
    10|    """快捷创建K线"""
    11|    o = open_ or low
    12|    c = close or ((high + low) / 2)
    13|    return {"open": o, "high": high, "low": low, "close": c}
    14|
    15|
    16|def test_simple_up_contain():
    17|    """用例1：简单向上包含"""
    18|    bars = [
    19|        make_bar(10, 8),     # K1: H=10, L=8
    20|        make_bar(9, 8.5),    # K2: H=9, L=8.5 (被K1包含)
    21|    ]
    22|    result = merge_kline_bars(bars)
    23|    assert len(result) == 1, f"应合并为1根，实际{len(result)}"
    24|    assert result[0]["high"] == 10
    25|    assert result[0]["low"] == 8.5, f"向上处理取较高的低点，应为8.5，实际{result[0]['low']}"
    26|
    27|
    28|def test_simple_down_contain():
    29|    """用例2：简单向下包含"""
    30|    bars = [
    31|        make_bar(10, 8),     # K1: H=10, L=8
    32|        make_bar(9, 8.5),    # K2: 反向包含K1
    33|    ]
    34|    # 方向判断需要前面有参照K线
    35|    bars_with_prev = [
    36|        make_bar(11, 7),     # 更前面一根，用于定方向
    37|        make_bar(10, 8),     # 向下
    38|        make_bar(9, 8.5),    # 被包含
    39|    ]
    40|    result = merge_kline_bars(bars_with_prev)
    41|    assert result[1]["high"] == 9, f"向下处理取较低的高点，应为9，实际{result[1]['high']}"
    42|    assert result[1]["low"] == 8.5
    43|
    44|
    45|def test_continuous_contain():
    46|    """用例3：连续包含"""
    47|    bars = [
    48|        make_bar(10, 8),     # K1
    49|        make_bar(9.5, 8.5),  # K2 包含于K1 → 向上处理
    50|        make_bar(9.8, 8.8),  # K3 包含于合并结果 → 向上处理
    51|    ]
    52|    result = merge_kline_bars(bars)
    53|    assert len(result) == 1
    54|    assert result[0]["high"] == 10
    55|    assert result[0]["low"] == 8.8, f"连续向上合并，低点应逐步抬高到8.8，实际{result[0]['low']}"
    56|
    57|
    58|def test_no_contain():
    59|    """不包含的情况：每根独立"""
    60|    bars = [
    61|        make_bar(10, 8),
    62|        make_bar(12, 9),
    63|        make_bar(14, 10),
    64|    ]
    65|    result = merge_kline_bars(bars)
    66|    assert len(result) == 3, "不包含的情况保持原样"
    67|
    68|
    69|def test_is_containing():
    70|    """包含判断函数"""
    71|    k1 = make_bar(10, 8)
    72|    k2 = make_bar(9, 8.5)
    73|    assert is_containing(k1, k2) == True
    74|    assert is_containing(k2, k1) == True
    75|
    76|    k3 = make_bar(12, 9)
    77|    assert is_containing(k1, k3) == False
    78|
    79|
    80|def test_reverse_mode():
    81|    """从右向左处理"""
    82|    bars = [
    83|        make_bar(10, 8),
    84|        make_bar(9, 8.5),
    85|    ]
    86|    result = merge_kline_bars(bars, reverse=True)
    87|    assert len(result) > 0, "reverse模式应正常返回"
    88|
    89|
    90|def test_empty_input():
    91|    """空输入"""
    92|    assert merge_kline_bars([]) == []
    93|
    94|
    95|def test_single_bar():
    96|    """单根K线"""
    97|    bars = [make_bar(10, 8)]
    98|    result = merge_kline_bars(bars)
    99|    assert len(result) == 1
   100|    assert result[0]["high"] == 10
   101|