# 股票价格监控自动交易工具

监控股票价格，当价格达到条件时，通过模拟鼠标键盘自动进行买入/卖出操作。

## 功能

- 实时监控指定股票价格
- 支持多种数据源（新浪财经、腾讯财经等）
- 价格达到阈值时发送桌面通知
- 自动模拟鼠标键盘操作完成交易
- 支持 Windows 系统

## 环境

- Python 3.8+
- Windows 10/11

## 安装

```bash
pip install -r requirements.txt
```

## 配置

编辑 `config.yaml` 文件：

```yaml
# 监控的股票列表
stocks:
  - code: "sh000001"
    name: "上证指数"
    high: 3500  # 高于此价格提醒
    low: 3000   # 低于此价格提醒
  - code: "sz000001"
    name: "平安银行"
    high: 15.0
    low: 12.0

# 刷新间隔（秒）
refresh_interval: 5

# 自动化设置
automation:
  enabled: true
  # 交易按钮位置（需要通过配置工具获取）
  buy_button: {x: 100, y: 200}
  sell_button: {x: 100, y: 250}
  price_input: {x: 100, y: 300}
  amount_input: {x: 100, y: 350}
  confirm_button: {x: 100, y: 400}
```

## 使用

1. 首先运行配置工具获取界面元素位置：
```bash
python position_finder.py
```

2. 运行主程序：
```bash
python main.py
```

3. 程序会：
   - 每隔 5 秒刷新股票价格
   - 价格达到阈值时发送 Windows 通知
   - 如果启用了自动化，点击确认后会执行模拟交易

## 项目结构

```
stock_monitor/
├── config.yaml          # 配置文件
├── main.py              # 主程序入口
├── stock_monitor.py     # 股票监控模块
├── automation.py        # 自动化操作模块
├── position_finder.py   # 坐标获取工具
├── requirements.txt     # 依赖
└── README.md            # 说明文档
```

## 注意事项

- 使用自动化功能前请先在测试环境验证
- 模拟交易存在风险，请谨慎使用
- 确保交易软件窗口在最前
