#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # Author：'BCY'
# # Time:2020/03/13  22:13

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 随机种子
np.random.seed(1)


def randrange(n, vmin, vmax):
    '''
    使数据分布均匀(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')  # 可进行多图绘制

# n = 500

# 对于每一组样式和范围设置，在由x在[23，32]、y在[0，100]、
# z在[zlow，zhigh]中定义的框中绘制n个随机点
# for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zlow, zhigh)
#     ax.scatter(xs, ys, zs, marker=m)  # 绘图

# plt.axis([10,30,0,10])

x = [28, 22, 15]
y = [10, 8, 6]
z = [10, 5, 4]

name = ['Shuttle', 'ToteRobot', 'Kiva']

ax = plt.figure().add_subplot(111,projection='3d')
ax.scatter(x, y, z,c='r',marker='o')
for i in range(len(x)):
    ax.text(x[i],y[i],z[i],name[i])

# ax.scatter(28, 10, 10, marker='o')  # 绘图
# ax.scatter(22, 8, 5, marker='^')  # 绘图
# ax.scatter(15, 6, 4)  # 绘图

# X、Y、Z的标签
ax.set_xlabel('Storage')
ax.set_ylabel('Throughtput')
ax.set_zlabel('Inverstment')

# plt.xlim((10,30)) #设置坐标轴的最大最小区间
# plt.ylim((0,10))#设置坐标轴的最大最小区间
# # plt.zlim((0,10)) #设置坐标轴的最大最小区间


plt.show()
