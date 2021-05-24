#!/usr/bin/env python
# coding: utf-8
"""图像采样示例

以一个 600*400 的测试图像做采样测试。

Usage:
    image_sampling.py [--ratio=<ratio>] [--method=<method>]

Options:
    -h, --help          帮助信息
    --ratio=<ratio>     采样比率 [default: 1]
    --method=<method>   采样方法，可选的方法有：
                        mean 均值采样
                        max 最大值采样
                        min 最小值采样
                        [default: mean]
"""

from itertools import product

from docopt import docopt
from skimage import data
from matplotlib import pyplot
import numpy as np


if __name__ == '__main__':
    docargs = docopt(__doc__)
    ratio = int(docargs['--ratio'])
    method = docargs['--method']

    source_image = data.coffee()
    target_image = np.zeros((
        int(source_image.shape[0]/ratio),
        int(source_image.shape[1]/ratio),
        int(source_image.shape[2]),
    ), dtype='int32')

    for i, j, k in product(*[range(_) for _ in target_image.shape]):
        # 获取采样图像块
        sampling_image = source_image[i*ratio:(i+1)*ratio, j*ratio:(j+1)*ratio]
        # 计算采样数据
        target_image[i][j] = {
            'mean': np.mean,
            'max': np.max,
            'min': np.min,
        }.get(method, np.mean)(sampling_image)

    pyplot.imshow(target_image)
    pyplot.show()

