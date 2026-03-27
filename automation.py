import time
import yaml
from pathlib import Path

try:
    import win32api
    import win32con
    import win32gui
except ImportError:
    print("警告: win32api 未安装，自动化功能将不可用")
    win32api = None


VK_CODES = {
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    '.': 0xBE,  # 小数点
}


class Automation:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
        self.enabled = self.config.get('automation', {}).get('enabled', False)
        self.positions = self.config.get('automation', {})
    
    def load_config(self):
        config_file = Path(self.config_path)
        if not config_file.exists():
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def click(self, x=None, y=None):
        if not win32api:
            return
        
        if x is not None and y is not None:
            x = int(x)
            y = int(y)
            print(f"点击位置: ({x}, {y})")
            win32api.SetCursorPos((x, y))
            time.sleep(0.1)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def double_click(self, x=None, y=None):
        if not win32api:
            return
        
        if x is not None and y is not None:
            x = int(x)
            y = int(y)
            win32api.SetCursorPos((x, y))
            time.sleep(0.1)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def type_text(self, text):
        if not win32api:
            return
        
        text = str(text)
        for char in text:
            vk = VK_CODES.get(char)
            if vk:
                win32api.keybd_event(vk, 0, 0, 0)
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.1)
    
    def input_stock_code(self, code):
        pos = self.positions.get('stock_input', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            print(f"输入股票代码: ({x}, {y})")
            self.double_click(x, y)
            time.sleep(0.2)
            self.type_text(str(code))
            time.sleep(0.3)
    
    def input_price(self, price):
        pos = self.positions.get('price_input', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            print(f"输入价格: ({x}, {y})")
            self.double_click(x, y)
            time.sleep(0.2)
            self.type_text(str(price))
            time.sleep(0.3)
    
    def input_amount(self, amount):
        pos = self.positions.get('amount_input', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            print(f"输入数量: ({x}, {y})")
            self.double_click(x, y)
            time.sleep(0.2)
            self.type_text(str(amount))
            time.sleep(0.3)
    
    def click_buy(self):
        pos = self.positions.get('buy_button', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            self.click(x, y)
            time.sleep(0.5)
    
    def click_sell(self):
        pos = self.positions.get('sell_button', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            self.click(x, y)
            time.sleep(0.5)
    
    def click_confirm(self):
        pos = self.positions.get('confirm_button', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            self.click(x, y)
            time.sleep(0.5)
    
    def open_app(self):
        pos = self.positions.get('open_app', {})
        x, y = int(pos.get('x', 0)), int(pos.get('y', 0))
        
        if x and y:
            print(f"打开软件: ({x}, {y})")
            self.click(x, y)
            time.sleep(1)
    
    def execute_buy(self, stock_code, price, amount=100):
        if not self.enabled:
            return False
        
        print(f"执行买入: 股票={stock_code}, 价格={price}, 数量={amount}")
        
        self.open_app()
        time.sleep(1)
        self.input_stock_code(stock_code)
        self.input_price(price)
        self.input_amount(amount)
        self.click_buy()
        time.sleep(0.5)
        self.click_confirm()
        
        return True
    
    def execute_sell(self, stock_code, price, amount=100):
        if not self.enabled:
            return False
        
        print(f"执行卖出: 股票={stock_code}, 价格={price}, 数量={amount}")
        
        self.input_stock_code(stock_code)
        self.input_price(price)
        self.input_amount(amount)
        self.click_confirm()
        
        return True


if __name__ == '__main__':
    auto = Automation()
    print("自动化测试 - 买入 000001 100股 价格 10.91")
    auto.execute_buy("000001", 10.91, 100)
