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

# 生成图表（展示所有自定义选项）
fig = plot_superplot(
    sp,
    output='example_customized.png',
    test='t-test',
    show_stats=True,
    
    # 图表基本信息
    figsize=(6, 5),
    title='SuperPlot: Control vs Treatment',
    title_fontsize=14,
    ylabel='Cell Fluorescence (AU)',
    ylabel_fontsize=12,
    xlabel='Treatment Group',
    xlabel_fontsize=12,
    xticklabelsize=11,
    yticklabelsize=11,
    
    # 点和形状
    point_size=80,        # 散点大小
    mean_marker_size=160, # 均值marker大小
    marker_shape='o',     # 'o'=圆形, 's'=方形, '^'=三角形
    
    # 背景和框线
    show_grid=True,
    grid_linewidth=0.5,
    grid_linestyle='--',
    spines_visible=(False, False, True, True),  # 只显示左右边框
    spines_linewidth=1,
    
    # 图例
    show_legend=True,
    legend_loc='upper left',
    legend_fontsize=10,
    
    # P值文字位置
    pvalue_loc=(0.5, 0.95),
    pvalue_fontsize=12,
    stats_n_loc=(0.5, 0.90),
    stats_n_fontsize=10,
)

print("\n图表已生成: example_customized.png")


# ============================================================
# 示例 2:  publication 风格（无网格，更简洁）
# ============================================================
fig2 = plot_superplot(
    sp,
    output='example_publication.png',
    test='t-test',
    show_stats=True,
    
    # 基础设置
    figsize=(5, 4.5),
    title='Treatment Effect',
    title_fontsize=13,
    ylabel='Fluorescence',
    ylabel_fontsize=12,
    xlabel='',
    
    # 点设置
    point_size=60,
    mean_marker_size=120,
    marker_shape='o',
    
    # 简洁风格
    style='simple',
    show_grid=False,
    spines_visible=(False, False, True, True),
    spines_linewidth=1.2,
    
    # 图例
    show_legend=True,
    legend_loc='upper left',
    legend_fontsize=9,
    
    # 文字位置微调
    pvalue_loc=(0.5, 0.96),
    pvalue_fontsize=11,
    stats_n_loc=(0.5, 0.91),
    stats_n_fontsize=9,
)

print("图表已生成: example_publication.png")


# ============================================================
# 示例 3: 完全自定义
# ============================================================
custom_colors = {
    'Exp1': '#E74C3C',  # 红色
    'Exp2': '#3498DB',  # 蓝色
}

fig3 = plot_superplot(
    sp,
    output='example_custom.png',
    test='Mann-Whitney',
    show_stats=True,
    
    figsize=(7, 6),
    title='My SuperPlot',
    title_fontsize=16,
    ylabel='Intensity',
    ylabel_fontsize=14,
    xlabel='Group',
    xlabel_fontsize=14,
    xticklabelsize=12,
    yticklabelsize=12,
    
    point_size=100,
    mean_marker_size=200,
    marker_shape='s',  # 方形
    
    show_grid=True,
    grid_linewidth=0.8,
    spines_visible=(True, True, True, True),  # 显示全部边框
    
    show_legend=True,
    legend_loc='upper right',
    legend_fontsize=11,
    
    colors=custom_colors,
    
    pvalue_loc=(0.5, 0.98),
    pvalue_fontsize=14,
)

print("图表已生成: example_custom.png")
print("\n=== 所有示例完成 ===")