#
# import tensorflow as tf
#
# a = tf.test.is_built_with_cuda()
# print(a)

# -*- coding: utf-8 -*-
"""
测试GPU的计算能力，测试tensorflow-GPU版是否安装正确
"""

import tensorflow as tf
import numpy as np
import time

value = np.random.randn(5000, 1000)
a = tf.constant(value)

b = a * a

c = 0
tic = time.time()
with tf.Session() as sess:
    for i in range(1000):
        sess.run(b)

        c += 1
        if c % 100 == 0:
            d = c / 10
            # print(d)
            print("计算进行%s%%" % d)

toc = time.time()
t_cost = toc - tic

print("测试所用时间%s" % t_cost)
print("Ubuntu上GPU为1050ti测试时间为7.99727988243103")