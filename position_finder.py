import time
import yaml
from pathlib import Path

try:
    import win32api
    import win32con
    import win32gui
except ImportError:
    print("错误: 需要安装 pywin32")
    print("运行: pip install pywin32")
    exit(1)


class PositionFinder:
    def __init__(self):
        self.positions = {}
        self.recording = False
    
    def get_cursor_pos(self):
        return win32api.GetCursorPos()
    
    def on_mouse_event(self, event, args):
        if self.recording:
            x, y = self.get_cursor_pos()
            print(f"当前位置: ({x}, {y})")
    
    def record_position(self, name):
        print(f"\n记录位置: {name}")
        print("将鼠标移动到目标位置，按 Enter 确认...")
        input()
        x, y = self.get_cursor_pos()
        self.positions[name] = {'x': x, 'y': y}
        print(f"已记录: {name} = ({x}, {y})")
        return self.positions[name]
    
    def save_positions(self, config_path='config.yaml'):
        config_file = Path(config_path)
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        
        if 'automation' not in config:
            config['automation'] = {}
        
        for key, pos in self.positions.items():
            config['automation'][key] = pos
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)
        
        print(f"\n位置已保存到 {config_path}")
    
    def run(self):
        print("=" * 50)
        print("股票交易坐标获取工具")
        print("=" * 50)
        print("\n请按顺序记录以下位置:")
        
        positions_to_record = [
            ('buy_button', '买入按钮'),
            ('sell_button', '卖出按钮'),
            ('price_input', '价格输入框'),
            ('amount_input', '数量输入框'),
            ('confirm_button', '确认按钮'),
        ]
        
        for key, desc in positions_to_record:
            self.record_position(desc)
        
        print("\n记录完成！")
        self.save_positions()
        
        print("\n记录的位置:")
        for key, pos in self.positions.items():
            print(f"  {key}: x={pos['x']}, y={pos['y']}")


if __name__ == '__main__':
    finder = PositionFinder()
    finder.run()
