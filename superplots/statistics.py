"""
统计检验模块
"""

import numpy as np
from scipy import stats
from typing import Dict, Tuple, Optional


class StatisticalTest:
    """
    统计检验类
    
    基于**实验重复**（而非细胞数）进行统计检验。
    这是 SuperPlots 的核心原则。
    """
    
    @staticmethod
    def ttest(
        group1: np.ndarray,
        group2: np.ndarray,
        paired: bool = False,
    ) -> Dict:
        """
        独立样本或配对 t 检验
        
        参数:
            group1: 组1的实验均值数组
            group2: 组2的实验均值数组
            paired: 是否配对检验
        
        返回:
            包含统计量的字典
        """
        if paired:
            if len(group1) != len(group2):
                raise ValueError("配对检验需要相同数量的样本")
            stat, p = stats.ttest_rel(group1, group2)
        else:
            stat, p = stats.ttest_ind(group1, group2)
        
        return {
            'test': 't-test' + ('_paired' if paired else '_independent'),
            'statistic': stat,
            'p_value': p,
            'n1': len(group1),
            'n2': len(group2),
            'mean1': np.mean(group1),
            'mean2': np.mean(group2),
            'sem1': stats.sem(group1),
            'sem2': stats.sem(group2),
        }
    
    @staticmethod
    def mann_whitney(
        group1: np.ndarray,
        group2: np.ndarray,
    ) -> Dict:
        """
        Mann-Whitney U 检验（非参数）
        """
        stat, p = stats.mannwhitneyu(group1, group2, alternative='two-sided')
        
        return {
            'test': 'Mann-Whitney U',
            'statistic': stat,
            'p_value': p,
            'n1': len(group1),
            'n2': len(group2),
            'mean1': np.mean(group1),
            'mean2': np.mean(group2),
        }
    
    @staticmethod
    def anova(
        *groups: np.ndarray,
    ) -> Dict:
        """
        单因素 ANOVA
        """
        stat, p = stats.f_oneway(*groups)
        
        return {
            'test': 'One-way ANOVA',
            'statistic': stat,
            'p_value': p,
            'n_groups': len(groups),
            'group_means': [np.mean(g) for g in groups],
        }
    
    @staticmethod
    def kruskal_wallis(
        *groups: np.ndarray,
    ) -> Dict:
        """
        Kruskal-Wallis 检验（非参数多组比较）
        """
        stat, p = stats.kruskal(*groups)
        
        return {
            'test': 'Kruskal-Wallis',
            'statistic': stat,
            'p_value': p,
            'n_groups': len(groups),
            'group_means': [np.mean(g) for g in groups],
        }
    
    @staticmethod
    def format_pvalue(p: float) -> str:
        """格式化 P 值显示"""
        if p < 0.001:
            return "P < 0.001"
        elif p < 0.01:
            return f"P = {p:.3f}"
        else:
            return f"P = {p:.2f}"