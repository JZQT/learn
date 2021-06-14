#!/usr/bin/env python
# coding: utf-8
"""图像量化示例

图像模拟量化测试。

Usage:
    quantization.py [--ratio=<ratio>] [--gray]

Options:
    -h, --help          帮助信息
    --ratio=<ratio>     量化比率，想要测试多个量化比率可用 , 分割
                        比如：2,4 [default: 1]
    --gray              灰度化，设置该参数会先将原图灰度化再处理
"""

from itertools import product

from docopt import docopt
from matplotlib import pyplot

from learn import data
from learn import utils
from learn.utils import compute_rows_and_cols, split_to_ints


if __name__ == '__main__':
    docargs = docopt(__doc__)
    ratios = split_to_ints(str(docargs['--ratio']), ",")
    if len(ratios) == 0:
        raise Exception(f"错误的 ratio 参数: {docargs['--ratio']}")

    images = [data.lena() for _ in range(len(ratios))]
    shape = images[0].shape
    if docargs['--gray']:
        for image in images:
            utils.graying(image, replace=True)

    rows, cols = compute_rows_and_cols(len(images))
    for idx, (ratio, image) in enumerate(zip(ratios, images)):
        for i, j, k in product(*[range(_) for _ in shape]):
            image[i][j][k] = int(image[i][j][k]/ratio)*ratio
        pyplot.subplot(rows, cols, idx+1)
        pyplot.title(f"ratio={ratio}")
        pyplot.imshow(image)

    pyplot.show()
