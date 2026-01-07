# Chart Generator

一个用于生成排序条形图的 Python 工具，支持通过配置文件自定义数据，导出 PNG、SVG 和 PPTX 格式。图表数据按从大到小（降序）排列。

## 功能特性

- 📊 自动生成排序条形图（降序排列，最大值在顶部）
- ⚙️ 支持通过 JSON 配置文件自定义数据、标题、标签等
- 📤 多格式导出：PNG、SVG、PPTX
- 🖼️ 动态调整图表布局，适配不同数据量
- 📋 支持命令行参数覆盖配置

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### 基本使用

使用默认配置文件生成图表：

```bash
python recreate_sorted_chart.py
```

### 使用自定义配置文件

```bash
python recreate_sorted_chart.py --config my_config.json
```

### 仅提供数据文件

创建一个只包含数据的 JSON 文件：

```json
[
  ["项目A", 1234.5],
  ["项目B", 987.3],
  ["项目C", 756.2]
]
```

然后运行：

```bash
python recreate_sorted_chart.py --data-file my_data.json
```

### 命令行参数覆盖

```bash
python recreate_sorted_chart.py --title "我的图表" --unit "万元" --tag "销售额"
```

### 允许覆盖 PPTX 文件

如果 `charts_presentation.pptx` 已存在，使用 `--overwrite-pptx` 参数覆盖：

```bash
python recreate_sorted_chart.py --overwrite-pptx
```

## 配置文件格式

配置文件包含以下字段：

```json
{
  "title": "图表标题",
  "tag": "数据标签",
  "unit": "单位",
  "left_summary": "左侧汇总标题",
  "data": [
    ["名称1", 数值1],
    ["名称2", 数值2]
  ]
}
```

**字段说明：**
- `title`: 图表顶部中央显示的主标题
- `tag`: 图表右上角显示的数据类型标签
- `unit`: 数据单位
- `left_summary`: 图表左上角显示的汇总标题
- `data`: 数据数组，每个元素为 `[名称, 数值]`

## 输出文件

生成的文件保存在 `outputs/` 目录：

- `chart_sorted.png` - 高分辨率 PNG 图片 (300 DPI)
- `chart_sorted.svg` - 矢量 SVG 图
- `charts_presentation.pptx` - PowerPoint 演示文稿

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--config` | 指定配置文件路径 |
| `--data-file` | 指定只包含数据的 JSON 文件 |
| `--title` | 覆盖配置文件中的标题 |
| `--tag` | 覆盖配置文件中的数据标签 |
| `--unit` | 覆盖配置文件中的单位 |
| `--left-summary` | 覆盖配置文件中的汇总标题 |
| `--output-dir` | 指定输出目录 |
| `--overwrite-pptx` | 允许覆盖已存在的 PPTX 文件 |

## 项目结构

```
chart_tools/
├── config.json             # 示例配置文件
├── recreate_sorted_chart.py # 图表生成主脚本
├── requirements.txt        # Python 依赖
├── .gitignore           # Git 忽略规则
└── README.md           # 项目说明
```

## 技术栈

- **Matplotlib** - 图表绘制
- **python-pptx** - PPTX 文件生成
- **Pillow** - 图像处理
- **NumPy** - 数值计算
