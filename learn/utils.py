# coding: utf-8

import math


def compute_rows_and_cols(count: int) -> (int, int):
    """根据要显示的图数量计算应该显示的行数和列数

    >>> compute_rows_and_cols(1)
    (1, 1)
    >>> compute_rows_and_cols(2)
    (1, 2)
    >>> compute_rows_and_cols(4)
    (2, 2)
    >>> compute_rows_and_cols(8)
    (3, 3)
    """
    rows = int(math.sqrt(count))
    if rows*rows >= count:
        return rows, rows
    cols = rows
    while True:
        cols += 1
        if rows*cols >= count:
            return rows, cols
        rows += 1
        if rows*cols >= count:
            return rows, cols
