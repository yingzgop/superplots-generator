"""
核心类：SuperPlot
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Union


class SuperPlot:
    """
    SuperPlot 主类
    
    用于处理细胞生物学实验数据，生成符合 SuperPlots 原则的可视化图表。
    
    参数:
        data: 数据文件路径 (Excel 或 CSV)
        x: 分组列名 (如 'group')
        y: 数值列名 (如 'value')
        experiment_col: 实验编号列名 (如 'experiment')
        groups: 要比较的处理组列表
    """
    
    def __init__(
        self,
        data: Union[str, pd.DataFrame],
        x: str,
        y: str,
        experiment_col: str,
        groups: Optional[List[str]] = None,
    ):
        # 加载数据
        if isinstance(data, pd.DataFrame):
            self.df = data.copy()
        elif isinstance(data, (str, Path)):
            if data.endswith('.csv'):
                self.df = pd.read_csv(data)
            elif data.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(data)
            else:
                raise ValueError("支持 CSV 或 Excel 文件")
        else:
            raise TypeError("data 必须是文件路径或 DataFrame")
        
        # 验证列名
        required_cols = [x, y, experiment_col]
        missing = [c for c in required_cols if c not in self.df.columns]
        if missing:
            raise ValueError(f"数据中缺少列: {missing}")
        
        self.x = x
        self.y = y
        self.experiment_col = experiment_col
        
        # 筛选指定组
        if groups:
            self.df = self.df[self.df[x].isin(groups)]
            self.groups = groups
        else:
            self.groups = self.df[x].unique().tolist()
        
        # 计算每个实验的统计量
        self._compute_experiment_stats()
    
    def _compute_experiment_stats(self):
        """计算每个实验的均值和整体统计量"""
        # 每个实验的均值
        self.exp_means = self.df.groupby([self.experiment_col, self.x])[self.y].mean().reset_index()
        
        # 整体均值和 SEM（基于实验数）
        exp_stats = self.df.groupby(self.experiment_col)[self.y].agg(['mean', 'std', 'count'])
        exp_stats['sem'] = exp_stats['std'] / np.sqrt(exp_stats['count'])
        
        self.stats_by_group = self.df.groupby(self.x)[self.y].agg(['mean', 'std', 'count'])
        
        # 计算实验级别的统计（符合 SuperPlots 原则）
        # 按实验分组，计算每个实验内各组的均值，然后用实验均值做统计
        self.experiment_means_by_group = {}
        for group in self.groups:
            group_data = self.df[self.df[self.x] == group]
            exp_means = group_data.groupby(self.experiment_col)[self.y].mean()
            self.experiment_means_by_group[group] = exp_means
    
    def get_experiment_means(self, group: str) -> np.ndarray:
        """获取指定组的实验均值数组（用于统计检验）"""
        if group not in self.experiment_means_by_group:
            raise ValueError(f"组 {group} 不存在")
        return self.experiment_means_by_group[group].values
    
    def get_summary(self) -> pd.DataFrame:
        """获取汇总统计"""
        summary = []
        for group in self.groups:
            exp_means = self.get_experiment_means(group)
            summary.append({
                'Group': group,
                'N_experiments': len(exp_means),
                'Mean_of_means': exp_means.mean(),
                'SEM': exp_means.std() / np.sqrt(len(exp_means)),
                'Overall_mean': self.df[self.df[self.x] == group][self.y].mean(),
                'N_cells': len(self.df[self.df[self.x] == group]),
            })
        return pd.DataFrame(summary)
    
    def __repr__(self):
        return f"SuperPlot(groups={self.groups}, n_exps={len(self.df[self.experiment_col].unique())})"