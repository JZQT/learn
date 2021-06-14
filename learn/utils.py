# coding: utf-8

import math
from typing import List
from itertools import product

import numpy as np


def split_to_ints(string: str, sep: str) -> List[int]:
    """字符串分割为整数列表

    空字符串会被忽略。

    >>> split_to_ints("1,2,4,8", ",")
    [1, 2, 4, 8]
    >>> split_to_ints("1,,4", ",")
    [1, 4]
    >>> split_to_ints("", ",")
    []
    """
    return [int(_) for _ in string.split(sep) if _]


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


def graying(img: np.ndarray, method: str = 'mean', replace: bool = False) -> np.ndarray:
    """灰度化图像处理"""
    shape = img.shape
    result = img
    if not replace:
        result = np.zeros(img.shape, dtype=img.dtype)
    for i, j in product(range(shape[0]), range(shape[1])):
        result[i][j] = {
            'mean': np.mean,
            'max': np.max,
            'min': np.min,
        }.get(method, np.mean)(img[i][j])
    return result


def sampling(img: np.ndarray, ratio: int) -> np.ndarray:
    """图像采样模拟"""
    result = np.zeros((
        int(img.shape[0]/ratio),
        int(img.shape[1]/ratio),
        img.shape[2],
    ), dtype=img.dtype)
    for i, j, k in product(*[range(_) for _ in result.shape]):
        # 获取采样图像块
        sampling_image = img[i*ratio:(i+1)*ratio, j*ratio:(j+1)*ratio]
        # 计算采样数据
        result[i][j] = sampling_image[0][0]
    return result
