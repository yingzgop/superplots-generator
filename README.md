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

# 创建图表
plot = SuperPlot(
    data="your_data.xlsx",
    x="group",
    y="value",
    experiment_col="experiment",
    groups=["Control", "Treatment"]
)

# 生成图表
plot.plot(
    output="superplot.png",
    test="t-test",  # 或 "Mann-Whitney", "ANOVA"
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
- ✅ 配对/非配对检验
- ✅ 支持 Excel/CSV 输入
- ✅ 可自定义配色、标签、风格

## 📝 API 参考

### SuperPlot 类

```python
SuperPlot(
    data: str,           # 数据文件路径
    x: str,              # 分组列名
    y: str,              # 数值列名
    experiment_col: str, # 实验编号列名
    groups: list,        # 要比较的组
)
```

### 方法

```python
# 生成图表
plot.plot(
    output: str,         # 输出文件路径
    test: str,           # 统计检验方法
    paired: bool,        # 是否配对检验
    show_stats: bool,    # 是否显示统计结果
    colors: dict,        # 自定义颜色
    style: str,          # 图表风格
)
```

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

## 📚 参考文献

- Lord SJ, et al. (2020) SuperPlots: Communicating reproducibility and variability in cell biology. J Cell Biol 219(6):e202001064.

## 📄 许可证

MIT License

---

*Created by Christina (牧濑红莉栖) for Yinski*
*El Psy Kongroo 🧪*