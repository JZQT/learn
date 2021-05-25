#!/usr/bin/env python
# coding: utf-8
"""图像量化示例

以一个 600*400 的测试图像做量化测试。

Usage:
    image_quantization.py [--ratio=<ratio>]

Options:
    -h, --help          帮助信息
    --ratio=<ratio>     量化比率，想要测试多个量化比率可用 , 分割
                        比如：2,4 [default: 1]
"""

from itertools import product

from docopt import docopt
from skimage import data
from matplotlib import pyplot

from utils import compute_rows_and_cols


if __name__ == '__main__':
    docargs = docopt(__doc__)
    ratios = [int(_) for _ in str(docargs['--ratio']).split(",")]
    if len(ratios) == 0:
        raise Exception(f"错误的 ratio 参数: {docargs['--ratio']}")

    images = [data.coffee() for _ in range(len(ratios))]

    for ratio, image in zip(ratios, images):
        for i, j, k in product(*[range(_) for _ in images[0].shape]):
            image[i][j][k] = int(image[i][j][k]/ratio)*ratio

    rows, cols = compute_rows_and_cols(len(images))

    for idx, (ratio, image) in enumerate(zip(ratios, images)):
        pyplot.subplot(rows, cols, idx+1)
        pyplot.title(f"QuantizationRatio: {ratio}")
        pyplot.imshow(image)

    pyplot.show()
