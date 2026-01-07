# Chart Generator

一个用于生成排序条形图的 Python 工具，支持导出 PNG、SVG 和 PPTX 格式。图表数据按从大到小（降序）排列。

## 功能特性

- 📊 自动生成排序条形图（降序排列，最大值在顶部）
- 🎨 支持自定义标题、标签和单位
- 📤 多格式导出：PNG、SVG、PPTX
- 🚀 提供 REST API 服务
- 🖼️ 动态调整图表布局，适配不同数据量

## 安装依赖

```bash
pip install -r requirements-rest.txt
```

## 使用方式

### 命令行使用

1. 创建 JSON 配置文件（参考 `config_example.json`）：

```json
{
  "title": "各业务员回款金额对比分析",
  "tag": "回款金额",
  "unit": "万元",
  "left_summary": "总回款金额",
  "data": [
    ["李艳华", 8638.0],
    ["郑群", 2418.3],
    ["胡军可", 2397.3]
  ]
}
```

2. 运行生成命令：

```bash
python recreate_sorted_chart.py --config config_example.json
```

3. 使用 `--overwrite-pptx` 参数允许覆盖已存在的 PPTX 文件：

```bash
python recreate_sorted_chart.py --config config_example.json --overwrite-pptx
```

### REST API 服务

**启动服务：**

```bash
python rest_server.py
```

访问 API 文档：http://127.0.0.1:8000/docs

**API 端点：**

- `POST /generate?fmt={format}`

**参数说明：**

- `fmt`: 输出格式，可选值：
  - `png` - 仅返回 PNG 图片
  - `svg` - 仅返回 SVG 矢量图
  - `pptx` - 仅返回 PPTX 演示文稿
  - `all` - 返回包含所有格式的 ZIP 压缩包

**测试命令：**

```bash
curl -X POST "http://127.0.0.1:8000/generate?fmt=all" \
  -H "Content-Type: application/json" \
  --data-binary @config_example.json \
  -o outputs/generate_response.zip
```

## 输出文件

生成的文件保存在 `outputs/` 目录：

- `chart_sorted.png` - 高分辨率 PNG 图片 (300 DPI)
- `chart_sorted.svg` - 矢量 SVG 图
- `charts_presentation.pptx` - PowerPoint 演示文稿

## 项目结构

```
chart_tools/
├── scripts/              # 辅助脚本
│   └── inspect_image.py  # 图像检查工具
├── outputs/              # 输出目录
├── config_example.json   # 配置示例
├── recreate_sorted_chart.py  # 图表生成主脚本
├── rest_server.py        # REST API 服务
├── requirements-rest.txt # Python 依赖
└── README.md            # 项目说明
```

## 技术栈

- **FastAPI** - REST API 框架
- **Matplotlib** - 图表绘制
- **python-pptx** - PPTX 文件生成
- **Pillow** - 图像处理
