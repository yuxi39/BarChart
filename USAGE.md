Usage
-----

1. Create a JSON config similar to `config_example.json`:

```
{
  "title": "各业务员回款金额对比分析",
  "tag": "回款金额",
  "unit": "万元",
  "left_summary": "总回款金额",
  "data": [["李艳华", 8638.0], ["郑群", 2418.3]]
}
```

2. Run:

```
python recreate_sorted_chart.py --config config_example.json
```

3. Or provide just the data file:

```
python recreate_sorted_chart.py --data-file my_data.json
```

4. Use `--overwrite-pptx` to allow replacing an existing `charts_presentation.pptx`.
