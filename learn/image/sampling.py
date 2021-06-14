#!/usr/bin/env python
# coding: utf-8
"""图像采样示例

图像模拟采样测试。

Usage:
    sampling.py [--ratio=<ratio>] [--method=<method>] [--gray]

Options:
    -h, --help          帮助信息
    --ratio=<ratio>     采样比率 [default: 1]
    --gray              灰度化，设置该参数会先将原图灰度化再处理
    --method=<method>   采样方法，可选的方法有：
                        mean 均值采样
                        max 最大值采样
                        min 最小值采样
                        [default: mean]
"""

from itertools import product

from docopt import docopt
from matplotlib import pyplot

from learn.data import lena
from learn.utils import split_to_ints, compute_rows_and_cols, sampling, graying


if __name__ == '__main__':
    docargs = docopt(__doc__)
    ratios = split_to_ints(str(docargs['--ratio']), ",")
    methods = str(docargs['--method']).split(",")

    source_image = lena()
    if docargs['--gray']:
        graying(source_image, replace=True)

    rows, cols = compute_rows_and_cols(len(ratios)*len(methods))

    for idx, (method, ratio) in enumerate(product(methods, ratios)):
        image = sampling(source_image, ratio)
        pyplot.subplot(rows, cols, idx+1)
        pyplot.title(f"method={method}, ratio={ratio}")
        pyplot.imshow(image)

    pyplot.show()
