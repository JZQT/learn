# coding: utf-8

import numpy as np
import skimage.io


def lena() -> np.ndarray:
    """返回 lena 图"""
    return skimage.io.imread("resource/lena.png")
