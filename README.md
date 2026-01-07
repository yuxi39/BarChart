# Chart Tools

图表生成工具，支持从 JSON 配置生成排序的横向柱状图，输出 PNG、SVG 和 PPTX 格式。

## 功能特性

- 📊 自动生成排序的横向柱状图（从大到小排列）
- 🎨 支持自定义标题、标签、单位和左侧汇总标签
- 📁 支持多种输出格式：PNG（300 DPI）、SVG（矢量）、PPTX
- ⚙️ 灵活的配置方式：命令行参数、JSON 配置文件
- 🚀 REST API 服务支持
- 📝 适配不同数据量的自动布局调整

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### 1. 命令行使用

#### 使用默认配置生成图表

```bash
python recreate_sorted_chart.py
```

#### 使用配置文件

```bash
python recreate_sorted_chart.py --config config.json
```

#### 使用单独的数据文件

```bash
python recreate_sorted_chart.py --data-file my_data.json
```

#### 通过命令行参数覆盖配置

```bash
python recreate_sorted_chart.py --title "自定义标题" --tag "数据值" --unit "万元" --left-summary "总计"
```

#### 指定输出目录

```bash
python recreate_sorted_chart.py --output-dir ./my_outputs
```

#### 覆盖已存在的 PPTX 文件

```bash
python recreate_sorted_chart.py --overwrite-pptx
```

### 2. REST API 使用

#### 启动服务

```bash
python rest_server.py
```

服务将在 `http://127.0.0.1:8000` 启动。

#### API 文档

访问 `http://127.0.0.1:8000/docs` 查看 Swagger 文档。

#### 生成图表

**请求格式：**

```bash
curl -X POST "http://127.0.0.1:8000/generate?fmt=png" \
  -H "Content-Type: application/json" \
  -d @config.json \
  -o output.png
```

**支持的格式参数：**
- `png`: 返回 PNG 图片
- `svg`: 返回 SVG 矢量图
- `pptx`: 返回 PowerPoint 文件
- `all`: 返回包含所有格式的 ZIP 压缩包

**请求示例：**

```bash
# 生成 PNG
curl -X POST "http://127.0.0.1:8000/generate?fmt=png" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "示例数据对比分析",
    "tag": "数据值",
    "unit": "单位",
    "left_summary": "总计",
    "data": [["项目A", 1234.5], ["项目B", 987.3]]
  }' \
  -o chart.png

# 生成所有格式的 ZIP
curl -X POST "http://127.0.0.1:8000/generate?fmt=all" \
  -H "Content-Type: application/json" \
  -d @config.json \
  -o chart_bundle.zip
```

## 配置文件格式

### 完整配置示例 (config_example.json)

```json
{
  "title": "示例数据对比分析",
  "tag": "数据值",
  "unit": "单位",
  "left_summary": "总计",
  "data": [
    ["项目A", 1234.5],
    ["项目B", 987.3],
    ["项目C", 756.2],
    ["项目D", 543.1],
    ["项目E", 321.0]
  ]
}
```

### 配置字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 否 | 图表标题，默认："示例数据对比分析" |
| `tag` | string | 否 | 右侧标签，默认："数据值" |
| `unit` | string | 否 | 数值单位，默认："单位" |
| `left_summary` | string | 否 | 左侧汇总标签，默认："总计" |
| `data` | list/dict | 否 | 数据，可以是列表 `[[名称, 值], ...]` 或字典 `{"名称": 值, ...}` |

### 数据格式

**列表格式：**
```json
"data": [
  ["项目A", 1234.5],
  ["项目B", 987.3]
]
```

**字典格式：**
```json
"data": {
  "项目A": 1234.5,
  "项目B": 987.3
}
```

## 输出文件

运行后将在输出目录生成以下文件：

- `chart_sorted.png`: 高分辨率 PNG 图片 (300 DPI)
- `chart_sorted.svg`: SVG 矢量图
- `charts_presentation.pptx`: PowerPoint 演示文稿

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--config` | JSON 配置文件路径 | - |
| `--data-file` | 数据文件路径 | - |
| `--title` | 图表标题（覆盖配置） | - |
| `--tag` | 右侧标签（覆盖配置） | - |
| `--unit` | 数值单位（覆盖配置） | - |
| `--left-summary` | 左侧汇总标签（覆盖配置） | - |
| `--output-dir` | 输出目录 | `outputs` |
| `--overwrite-pptx` | 允许覆盖 PPTX | `False` |

## 配置文件使用建议

- `config_example.json`: 示例配置文件，提交到仓库
- `config.json`: 你的实际配置文件，不会被 git 提交（见 .gitignore）

## 注意事项

1. 字体支持：依赖系统中安装的微软雅黑 (Microsoft YaHei) 字体
2. PPTX 文件：如果文件已打开，会生成 `charts_presentation_v2.pptx` 作为备选
3. REST API：临时文件会在请求后自动清理

## 项目结构

```
chart_tools/
├── recreate_sorted_chart.py   # 主程序：图表生成
├── rest_server.py              # REST API 服务器
├── requirements.txt            # Python 依赖
├── config_example.json         # 示例配置文件
├── .gitignore                 # Git 忽略规则
└── outputs/                   # 输出目录（自动创建）
    ├── chart_sorted.png
    ├── chart_sorted.svg
    └── charts_presentation.pptx
```
