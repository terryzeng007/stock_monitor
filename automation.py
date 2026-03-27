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
    
    def move_mouse(self, x, y):
        if not win32api:
            return
        win32api.SetCursorPos((x, y))
    
    def click(self, x=None, y=None):
        if not win32api:
            return
        
        if x is not None and y is not None:
            win32api.SetCursorPos((x, y))
            time.sleep(0.1)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def double_click(self, x=None, y=None):
        if not win32api:
            return
        
        if x is not None and y is not None:
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
        
        for char in text:
            code = ord(char)
            win32api.keybd_event(code, 0, 0, 0)
            win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)
    
    def input_price(self, price):
        pos = self.positions.get('price_input', {})
        x, y = pos.get('x', 0), pos.get('y', 0)
        
        if x and y:
            self.double_click(x, y)
            time.sleep(0.2)
            self.type_text(str(price))
    
    def input_amount(self, amount):
        pos = self.positions.get('amount_input', {})
        x, y = pos.get('x', 0), pos.get('y', 0)
        
        if x and y:
            self.double_click(x, y)
            time.sleep(0.2)
            self.type_text(str(amount))
    
    def click_buy(self):
        pos = self.positions.get('buy_button', {})
        x, y = pos.get('x', 0), pos.get('y', 0)
        
        if x and y:
            self.click(x, y)
            time.sleep(0.3)
    
    def click_sell(self):
        pos = self.positions.get('sell_button', {})
        x, y = pos.get('x', 0), pos.get('y', 0)
        
        if x and y:
            self.click(x, y)
            time.sleep(0.3)
    
    def click_confirm(self):
        pos = self.positions.get('confirm_button', {})
        x, y = pos.get('x', 0), pos.get('y', 0)
        
        if x and y:
            self.click(x, y)
            time.sleep(0.3)
    
    def execute_buy(self, price, amount=100):
        if not self.enabled:
            return False
        
        print(f"执行买入: 价格={price}, 数量={amount}")
        
        self.click_buy()
        self.input_price(price)
        self.input_amount(amount)
        self.click_confirm()
        
        return True
    
    def execute_sell(self, price, amount=100):
        if not self.enabled:
            return False
        
        print(f"执行卖出: 价格={price}, 数量={amount}")
        
        self.click_sell()
        self.input_price(price)
        self.input_amount(amount)
        self.click_confirm()
        
        return True


if __name__ == '__main__':
    auto = Automation()
    print("自动化测试")
    print("点击鼠标左键测试...")
    auto.click(100, 100)
