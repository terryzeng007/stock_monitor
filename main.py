import sys
import time
import signal
from pathlib import Path

from stock_monitor import StockMonitor
from automation import Automation


class Application:
    def __init__(self):
        self.monitor = None
        self.automation = None
        self.running = False
    
    def load_config(self):
        config_file = Path('config.yaml')
        if not config_file.exists():
            print("错误: 配置文件 config.yaml 不存在")
            print("请先创建配置文件，或运行 position_finder.py 获取坐标")
            sys.exit(1)
    
    def setup_signal_handler(self):
        def signal_handler(sig, frame):
            print("\n收到退出信号，正在停止...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start(self):
        self.load_config()
        self.setup_signal_handler()
        
        self.monitor = StockMonitor()
        self.automation = Automation()
        
        print("=" * 50)
        print("股票价格监控自动交易系统")
        print("=" * 50)
        print(f"监控股票数: {len(self.monitor.stocks)}")
        print(f"刷新间隔: {self.monitor.refresh_interval} 秒")
        print(f"自动化: {'已启用' if self.automation.enabled else '未启用'}")
        print("=" * 50)
        
        self.running = True
        self.monitor.start()
        
        print("\n监控运行中，按 Ctrl+C 停止\n")
        
        while self.running:
            time.sleep(1)
    
    def stop(self):
        self.running = False
        if self.monitor:
            self.monitor.stop()
        print("程序已退出")


def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()
