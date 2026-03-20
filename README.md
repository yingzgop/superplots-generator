# SuperPlots Generator

一个用于生成 **SuperPlots**（超图）的 Python 工具，帮助细胞生物学实验数据可视化并正确展示统计可重复性。

## 📊 什么是 SuperPlots？

SuperPlots 同时展示：
- 所有数据点（散点图）
- 按实验分组的颜色编码
- 基于**生物重复**（独立实验）的统计检验

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备数据

数据文件格式（Excel 或 CSV）：

| group | experiment | value |
|-------|------------|-------|
| Control | Exp1 | 10.5 |
| Control | Exp1 | 11.2 |
| Control | Exp2 | 9.8 |
| Treatment | Exp1 | 15.3 |
| Treatment | Exp1 | 14.9 |
| Treatment | Exp2 | 16.1 |

- `group`: 处理组（如 Control, Treatment）
- `experiment`: 实验编号（区分生物学重复）
- `value`: 测量值

### 3. 运行

```python
from superplots import SuperPlot
from superplots.visualization import plot_superplot

# 创建 SuperPlot
sp = SuperPlot(
    data="your_data.xlsx",
    x="group",
    y="value",
    experiment_col="experiment",
    groups=["Control", "Treatment"]
)

# 生成图表
plot_superplot(
    sp,
    output="superplot.png",
    test="t-test",
    show_stats=True
)
```

## 📁 项目结构

```
superplots-generator/
├── superplots/
│   ├── __init__.py
│   ├── core.py          # 核心类
│   ├── statistics.py    # 统计检验
│   └── visualization.py # 可视化
├── tests/               # 单元测试
├── examples/            # 示例代码
├── requirements.txt     # 依赖
├── setup.py            # 安装配置
└── README.md
```

## 🎨 功能特性

- ✅ 散点图 + 颜色编码（按实验分组）
- ✅ 自动计算实验均值和 SEM
- ✅ 支持多种统计检验（t-test, Mann-Whitney, ANOVA）
- ✅ 支持 Excel/CSV 输入

### 可自定义选项

| 类别 | 参数 | 说明 |
|------|------|------|
| **图表基础** | `figsize`, `title`, `title_fontsize` | 图表尺寸和标题 |
| **坐标轴** | `xlabel`, `ylabel`, `xlabel_fontsize`, `ylabel_fontsize`, `xticklabelsize`, `yticklabelsize` | 坐标轴标签和刻度字体 |
| **点样式** | `point_size`, `mean_marker_size`, `marker_shape` | 散点和均值marker的大小和形状 |
| **背景网格** | `show_grid`, `grid_linewidth`, `grid_linestyle` | 网格显示和样式 |
| **边框** | `spines_visible`, `spines_linewidth` | 边框显示和粗细 |
| **图例** | `show_legend`, `legend_loc`, `legend_fontsize` | 图例显示和位置 |
| **统计文字** | `pvalue_loc`, `pvalue_fontsize`, `stats_n_loc`, `stats_n_fontsize` | P值和n值的显示位置和字体 |

### marker_shape 选项
- `'o'` - 圆形（默认）
- `'s'` - 方形
- `'^'` - 三角形
- `'D'` - 菱形

### spines_visible 选项
- 元组格式：`(top, right, bottom, left)`
- 例如：`(False, False, True, True)` - 只显示下边框和左边框

## 📦 支持的统计检验

| 方法 | 描述 | 适用场景 |
|------|------|---------|
| t-test | 独立样本 t 检验 | 两组正态分布数据 |
| paired-t | 配对 t 检验 | 配对/ matched 数据 |
| Mann-Whitney | Mann-Whitney U 检验 | 非正态分布/小样本 |
| ANOVA | 单因素方差分析 | 多组比较 |
| Kruskal-Wallis | Kruskal-Wallis 检验 | 非参数多组比较 |

## 🎯 统计可重复性要点

> ⚠️ **重要**：本工具默认按 `experiment_col` 列识别**生物重复**，统计检验使用实验数作为 n，而非细胞数。这符合 SuperPlots 的核心原则。

## 📝 示例代码

详见 `examples/example_basic.py`

```python
fig = plot_superplot(
    sp,
    output='custom_plot.png',
    test='t-test',
    show_stats=True,
    
    # 基础设置
    figsize=(6, 5),
    title='My SuperPlot',
    title_fontsize=14,
    ylabel='Fluorescence',
    ylabel_fontsize=12,
    
    # 点样式
    point_size=80,
    mean_marker_size=160,
    marker_shape='o',
    
    # 背景和边框
    show_grid=True,
    grid_linewidth=0.5,
    spines_visible=(False, False, True, True),
    
    # 图例
    show_legend=True,
    legend_loc='upper left',
    
    # 统计文字
    pvalue_loc=(0.5, 0.95),
    pvalue_fontsize=12,
)
```

## 📚 参考文献

- Lord SJ, et al. (2020) SuperPlots: Communicating reproducibility and variability in cell biology. J Cell Biol 219(6):e202001064.

## 📄 许可证

MIT License

---

*Created by Christina (牧濑红莉栖) for Yinski*
*El Psy Kongroo 🧪*