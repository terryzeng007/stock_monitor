import time
import threading
import requests
import yaml
from datetime import datetime
from pathlib import Path

try:
    from win10toast import ToastNotifier
except ImportError:
    ToastNotifier = None


class StockMonitor:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
        self.stocks = self.config.get('stocks', [])
        self.refresh_interval = self.config.get('refresh_interval', 5)
        self.last_prices = {}
        self.running = False
        
        if ToastNotifier:
            self.toaster = ToastNotifier()
        else:
            self.toaster = None
    
    def load_config(self):
        config_file = Path(self.config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件 {self.config_path} 不存在")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def fetch_price(self, stock_code):
        try:
            url = f"http://hq.sinajs.cn/list={stock_code}"
            
            headers = {
                'Referer': 'https://finance.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text
                if '=' in content:
                    data = content.split('=')[1].strip('"')
                    parts = data.split(',')
                    if len(parts) > 1:
                        name = parts[0]
                        price = float(parts[1])
                        return {'name': name, 'price': price}
            return None
        except Exception as e:
            print(f"获取股票 {stock_code} 价格失败: {e}")
            return None
    
    def check_alert(self, stock, current_price):
        code = stock['code']
        name = stock.get('name', code)
        
        high = stock.get('high')
        low = stock.get('low')
        
        triggered = []
        
        if high and current_price >= high:
            triggered.append(f"【{name}】价格达到 {current_price}，超过高价 {high}")
        
        if low and current_price <= low:
            triggered.append(f"【{name}】价格跌至 {current_price}，低于低价 {low}")
        
        return triggered
    
    def show_notification(self, title, message):
        if self.toaster:
            try:
                self.toaster.show_toast(title, message, duration=5)
            except:
                print(f"通知: {title} - {message}")
        else:
            print(f"通知: {title} - {message}")
    
    def monitor_loop(self):
        print(f"开始监控 {len(self.stocks)} 只股票...")
        
        while self.running:
            for stock in self.stocks:
                code = stock['code']
                result = self.fetch_price(code)
                
                if result:
                    price = result['price']
                    name = result['name']
                    current_time = datetime.now().strftime("%H:%M:%S")
                    
                    print(f"[{current_time}] {name}: {price}")
                    
                    alerts = self.check_alert(stock, price)
                    for alert in alerts:
                        print(f"ALERT: {alert}")
                        self.show_notification("股票监控提醒", alert)
                    
                    self.last_prices[code] = price
            
            time.sleep(self.refresh_interval)
    
    def start(self):
        self.running = True
        thread = threading.Thread(target=self.monitor_loop, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        self.running = False
        print("监控已停止")


if __name__ == '__main__':
    monitor = StockMonitor()
    print("股票监控系统启动")
    print("按 Ctrl+C 停止")
    
    try:
        monitor.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
