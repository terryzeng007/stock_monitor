---
name: stock-trading
description: 股票价格监控自动交易工具 - 监控股票价格并通过模拟鼠标键盘自动下单
license: MIT
compatibility: opencode
metadata:
  audience: traders
  workflow: automation
---

## 功能

- 实时监控股票价格（通过新浪财经API）
- 价格达到阈值时发送桌面通知
- 通过模拟鼠标键盘自动执行买入/卖出操作
- 支持配置多个股票和价格条件

## 项目位置

克隆项目后位于：`stock_monitor`

## 配置文件

`config.yaml` 配置说明：

```yaml
stocks:
  - code: "sz000001"      # 股票代码 (sz=深圳, sh=上海)
    name: "平安银行"
    high: 15.0            # 高于该价格提醒
    low: 10.0             # 低于该价格提醒

refresh_interval: 5       # 刷新间隔（秒）

automation:
  enabled: true           # 启用自动化
  stock_input: {x: 295, y: 125}    # 股票代码输入框
  buy_button: {x: 323, y: 245}    # 买入按钮
  price_input: {x: 278, y: 163}    # 价格输入框
  amount_input: {x: 297, y: 222}  # 数量输入框
  confirm_button: {x: 920, y: 668} # 确认按钮
  open_app: {x: 416, y: 1055}      # 打开软件位置
```

## 安装

```bash
git clone https://github.com/terryzeng007/stock_monitor.git
cd stock_monitor
pip install pywin32 pyyaml requests
```

## 使用方法

1. 先运行鼠标坐标获取工具获取界面元素位置：
   ```bash
   python mouse_gui.py
   ```
2. 修改 `config.yaml` 配置股票、坐标
3. 运行主程序：
   ```bash
   python main.py
   ```

## 依赖

- Python 3.8+
- pywin32
- pyyaml
- requests
