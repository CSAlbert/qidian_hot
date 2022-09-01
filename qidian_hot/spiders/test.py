# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/9/1 19:54
@File     : test.py
@Describe : TODO
"""


def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:", res)


g = foo()


print(next(g))
print("*" * 20)
print(next(g))
print(next(g))