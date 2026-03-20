"""
可视化模块
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from typing import Optional, Dict, List, Tuple
from .core import SuperPlot
from .statistics import StatisticalTest


# 默认配色方案（适合 SuperPlots）
DEFAULT_COLORS = {
    'Exp1': '#FFC107',  # 琥珀黄
    'Exp2': '#9E9E9E',  # 灰色
    'Exp3': '#2196F3',  # 蓝色
    'Exp4': '#4CAF50',  # 绿色
    'Exp5': '#E91E63',  # 粉色
    'Exp6': '#9C27B0',  # 紫色
}


def get_experiment_colors(experiments: List[str]) -> Dict[str, str]:
    """为每个实验分配颜色"""
    colors = {}
    for i, exp in enumerate(experiments):
        if exp in DEFAULT_COLORS:
            colors[exp] = DEFAULT_COLORS[exp]
        else:
            # 循环使用默认颜色
            color_keys = list(DEFAULT_COLORS.keys())
            colors[exp] = DEFAULT_COLORS[color_keys[i % len(color_keys)]]
    return colors


def plot_superplot(
    superplot: SuperPlot,
    output: Optional[str] = None,
    test: str = 't-test',
    paired: bool = False,
    show_stats: bool = True,
    style: str = 'default',
    figsize: Tuple[float, float] = (6, 5),
    point_size: float = 80,
    title: str = '',
    ylabel: str = '',
    xlabel: str = '',
    colors: Optional[Dict] = None,
) -> plt.Figure:
    """
    生成 SuperPlot 图表
    
    参数:
        superplot: SuperPlot 实例
        output: 输出文件路径
        test: 统计检验方法 ('t-test', 'Mann-Whitney', 'ANOVA')
        paired: 是否配对检验
        show_stats: 是否显示统计结果
        style: 图表风格
        figsize: 图形尺寸
        point_size: 散点大小
        title: 图表标题
        ylabel: Y轴标签
        xlabel: X轴标签
        colors: 自定义颜色字典
    
    返回:
        matplotlib Figure 对象
    """
    # 设置风格
    if style == 'default':
        plt.style.use('seaborn-v0_8-whitegrid')
    elif style == 'publication':
        _setup_publication_style()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # 获取实验列表和颜色
    experiments = superplot.df[superplot.experiment_col].unique().tolist()
    if colors is None:
        exp_colors = get_experiment_colors(experiments)
    else:
        exp_colors = colors
    
    # 绘制散点图
    for exp in experiments:
        exp_data = superplot.df[superplot.df[superplot.experiment_col] == exp]
        for group in superplot.groups:
            group_data = exp_data[exp_data[superplot.x] == group]
            x_pos = superplot.groups.index(group)
            # 添加轻微随机偏移，避免点完全重叠
            x_jitter = np.random.uniform(-0.15, 0.15)
            ax.scatter(
                x_pos + x_jitter,
                group_data[superplot.y].values,
                c=exp_colors[exp],
                s=point_size,
                alpha=0.7,
                edgecolors='white',
                linewidths=0.5,
                label=exp if group == superplot.groups[0] else '',
                zorder=3,
            )
    
    # 绘制实验均值（较大的点）
    for group in superplot.groups:
        group_exp_means = superplot.exp_means[
            superplot.exp_means[superplot.x] == group
        ]
        x_pos = superplot.groups.index(group)
        ax.scatter(
            x_pos,
            group_exp_means[superplot.y].values,
            c='black',
            s=point_size * 2,
            marker='D',
            alpha=0.9,
            edgecolors='white',
            linewidths=1,
            zorder=4,
        )
    
    # 绘制组均值和误差棒（基于实验数）
    for group in superplot.groups:
        exp_means = superplot.get_experiment_means(group)
        mean = exp_means.mean()
        sem = np.std(exp_means) / np.sqrt(len(exp_means))
        
        x_pos = superplot.groups.index(group)
        ax.errorbar(
            x_pos, mean, yerr=sem,
            fmt='_',
            color='black',
            markersize=20,
            capsize=5,
            capthick=2,
            linewidth=2,
            zorder=5,
        )
    
    # 设置坐标轴
    ax.set_xticks(range(len(superplot.groups)))
    ax.set_xticklabels(superplot.groups)
    ax.set_xlim(-0.5, len(superplot.groups) - 0.5)
    
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title)
    
    # 统计检验
    if show_stats and len(superplot.groups) == 2:
        group1_means = superplot.get_experiment_means(superplot.groups[0])
        group2_means = superplot.get_experiment_means(superplot.groups[1])
        
        if test == 't-test':
            result = StatisticalTest.ttest(group1_means, group2_means, paired=paired)
        elif test == 'Mann-Whitney':
            result = StatisticalTest.mann_whitney(group1_means, group2_means)
        else:
            raise ValueError(f"不支持的检验方法: {test}")
        
        # 在图上显示 P 值
        p_text = StatisticalTest.format_pvalue(result['p_value'])
        ax.text(
            0.5, 0.95, p_text,
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=12, fontweight='bold',
        )
        
        # 添加统计方法注释
        test_name = result['test']
        ax.text(
            0.5, 0.90,
            f"n = {result['n1']}, {result['n2']} experiments",
            transform=ax.transAxes,
            ha='center', va='top',
            fontsize=10, style='italic',
        )
    
    # 图例
    handles = [mpatches.Patch(color=exp_colors[exp], label=exp) for exp in experiments]
    ax.legend(handles=handles, title='Experiment', loc='upper left', framealpha=0.9)
    
    plt.tight_layout()
    
    # 保存
    if output:
        fig.savefig(output, dpi=300, bbox_inches='tight')
        print(f"图表已保存至: {output}")
    
    return fig


def _setup_publication_style():
    """设置发表级图表风格"""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'axes.linewidth': 1,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })