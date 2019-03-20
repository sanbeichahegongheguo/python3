import numpy as np 
import matplotlib.pyplot as plt


S1 = np.array([2572, 2483, 2302, 2125, 1990, 1853, 1694, 1400, 1134, 982, 869, 776, 668, 584, 480])*2
# 为了把图做大一点，把圆扩大了一倍
x1 = [(3/2)*np.pi+np.pi/(len(S1)+1)*(i+1) for i in range(2*(len(S1)+1)) if i<len(S1)]
# len(S1)+1 等于16 ， 因为python里计数从0开始，所以i+1起始加一，
# 又因为我们只有15个圆，所以我们生成的位置Y也只要十五个，所以加入限制条件<15

y1 = [180 for i in range(2*(len(S1)+1)) if i<len(S1) ]
# 我们继续生成15个y值，这样一来，我们三个参数都确定了，气泡了x轴位置，y轴位置，以及气泡大小
# 下面开始画图

fig = plt.figure(figsize=(13.44*2,7.5*2), facecolor='w')  # 建立一个画布
ax = fig.add_subplot(111, projection='polar', facecolor='w')  # 建立一个坐标系，projection='polar'表示极坐标
ax.scatter(x=x1, y=y1, s=S1, color=(180/255, 204/255,30/255), alpha=0.5, linewidths=0)  # 不要气泡有边框线，我们把linewidth设置为0
plt.ylim(0, 220)  # 限制y轴的显示大小

S2 = np.array([2028,1976,1962,1925,1904,1833,1730,1577,1524,1493,1475,1589,1511,1505,1524])*2
x2 = [(0)*np.pi+np.pi/(len(S1)+1)*(i+1) for i in range(2*(len(S1)+1))]
y2 = [130 for i in range(2*(len(S1)+1)) if i<len(S1) ]

H1 = [56, 55,54,52,51,50,49,47,43,40,37,34,31,28,24]
W1 = [0.05 for i in range(2*(len(S1)+1)) if i<len(S1)]
B = [30 for i in range(2*(len(S1)+1)) if i<len(S1)]

ax.bar(x=x1, height=H1, width=W1, bottom=B, color=(255/255, 171/255, 1/255))

ax.spines['polar'].set_visible(False)  # 去掉坐标轴的为外面一层粗的线
plt.grid(color='gray', linestyle=':', linewidth=1, which='major', axis='x', alpha=0.1)  # 添加网格线
ax.set_yticks([])  # 去掉 y轴上的文字
ax.set_xticks(x2)  # 应为网格线是跟着x轴走的，如果去掉x轴的话，网格线也就没了
ax.tick_params(axis='x', labelsize=0)  # 因为我们保留了x轴，x轴上的文字会存在，所以把x轴上的文字大小设置为0

# import matplotlib.font_manager
# font=matplotlib.font_manager.FontProperties(fname='D:\\Fonts\\English\\Museo700-Regular.otf')

for i in range(len(x1)):
    ax.text(x=x1[i], y=y1[i], s=S1[i], color='gray', ha='center', va='center', fontsize=12)
for i in range(len(x1)):
    ax.text(x=x1[i], y=y2[i], s=S2[i], color='gray', ha='center', va='center', fontsize=12)
for i in range(len(x1)):
    ax.text(x=x1[i], y=H1[i]+40, s="{}%".format(H1[i]), color='gray', ha='center', va='center', fontsize=12)

plt.show()
