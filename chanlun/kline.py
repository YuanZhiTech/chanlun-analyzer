     1|"""
     2|缠论K线包含处理模块
     3|
     4|参考：缠论第65课、第66课
     5|文档：docs/01_kline_merge.md
     6|"""
     7|
     8|from typing import List, Dict, Optional
     9|
    10|
    11|def merge_kline_bars(
    12|    bars: List[Dict[str, float]],
    13|    reverse: bool = False,
    14|) -> List[Dict[str, float]]:
    15|    """
    16|    对K线列表进行包含处理。
    17|
    18|    Args:
    19|        bars: K线数据列表，按时间升序排列（最早的在前）
    20|             每根K线格式: {"open": o, "high": h, "low": l, "close": c}
    21|        reverse: 是否从右向左处理（默认按时间顺序从左到右）
    22|
    23|    Returns:
    24|        包含处理后的K线列表
    25|    """
    26|    if not bars:
    27|        return []
    28|
    29|    work = list(bars)
    30|    if reverse:
    31|        work = list(reversed(work))
    32|
    33|    merged = []  # 存放处理好的K线
    34|    current = work[0]  # 当前处理基准K线
    35|    current_dir = None  # 当前方向: "up" / "down"
    36|
    37|    for i in range(1, len(work)):
    38|        k = work[i]
    39|
    40|        # 判断方向
    41|        if current_dir is None and len(merged) > 0:
    42|            prev = merged[-1]
    43|            cur = current
    44|        elif current_dir is None:
    45|            cur = current
    46|            prev = {}
    47|        else:
    48|            cur = current
    49|        
    50|        # 检查是否包含
    51|        is_contained = is_containing(current, k)
    52|
    53|        if is_contained:
    54|            # 需要方向来判断合并方式
    55|            if current_dir is None and len(merged) > 0:
    56|                prev = merged[-1]
    57|                current_dir = _calc_direction(prev, current)
    58|
    59|            if current_dir == "up":
    60|                current = {
    61|                    "open": current["open"],
    62|                    "high": max(current["high"], k["high"]),
    63|                    "low": max(current["low"], k["low"]),
    64|                    "close": k["close"],
    65|                }
    66|            elif current_dir == "down":
    67|                current = {
    68|                    "open": current["open"],
    69|                    "high": min(current["high"], k["high"]),
    70|                    "low": min(current["low"], k["low"]),
    71|                    "close": k["close"],
    72|                }
    73|            else:
    74|                # 方向不明，暂存
    75|                current = {
    76|                    "open": current["open"],
    77|                    "high": max(current["high"], k["high"]),
    78|                    "low": min(current["low"], k["low"]),
    79|                    "close": k["close"],
    80|                }
    81|        else:
    82|            # 不包含：当前K线加入结果，下一根成为新的基准
    83|            merged.append(current)
    84|            current = k
    85|            current_dir = None
    86|
    87|    # 处理最后一根
    88|    merged.append(current)
    89|
    90|    if reverse:
    91|        merged = list(reversed(merged))
    92|
    93|    return merged
    94|
    95|
    96|def is_containing(k1: Dict[str, float], k2: Dict[str, float]) -> bool:
    97|    """判断两根K线是否存在包含关系"""
    98|    # K1包含K2
    99|    if k1["high"] >= k2["high"] and k1["low"] <= k2["low"]:
   100|        return True
   101|    # K2包含K1
   102|    if k2["high"] >= k1["high"] and k2["low"] <= k1["low"]:
   103|        return True
   104|    return False
   105|
   106|
   107|def _calc_direction(prev: Dict[str, float], cur: Dict[str, float]) -> Optional[str]:
   108|    """计算方向"""
   109|    if cur["high"] > prev["high"] and cur["low"] > prev["low"]:
   110|        return "up"
   111|    if cur["high"] < prev["high"] and cur["low"] < prev["low"]:
   112|        return "down"
   113|    return None
   114|