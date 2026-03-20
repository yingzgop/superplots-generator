"""
示例 1: 基础用法
"""

import pandas as pd
from superplots import SuperPlot
from superplots.visualization import plot_superplot

# 创建示例数据
data = {
    'group': ['Control', 'Control', 'Control', 'Control', 'Control', 'Control',
              'Treatment', 'Treatment', 'Treatment', 'Treatment', 'Treatment', 'Treatment'],
    'experiment': ['Exp1', 'Exp1', 'Exp1', 'Exp2', 'Exp2', 'Exp2',
                   'Exp1', 'Exp1', 'Exp1', 'Exp2', 'Exp2', 'Exp2'],
    'value': [10.5, 11.2, 10.8, 9.8, 10.1, 10.3,
              15.3, 14.9, 15.1, 16.1, 15.8, 15.5]
}
df = pd.DataFrame(data)

# 创建 SuperPlot
sp = SuperPlot(
    data=df,
    x='group',
    y='value',
    experiment_col='experiment',
    groups=['Control', 'Treatment']
)

# 打印统计摘要
print("=== 数据摘要 ===")
print(sp.get_summary())

# 生成图表
fig = plot_superplot(
    sp,
    output='example_basic.png',
    test='t-test',
    show_stats=True,
    ylabel='Cell Fluorescence (AU)',
    title='SuperPlot: Control vs Treatment'
)

print("\n图表已生成: example_basic.png")