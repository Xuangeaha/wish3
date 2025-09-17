"""
祈愿 · 幸运观众：开发者指令窗口

Copyright © 2025 XuangeAha(轩哥啊哈OvO/卡猫kat)

"""

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import shlex

from RoundShadow import RoundShadow
from MovableWindow import MovableWindow
import MessageBox

from config import _iconpath, _default_lang

class DeveloperCommandWindow(MovableWindow):
    def __init__(self, wish_window, root_settings, parent=None):
        super(DeveloperCommandWindow, self).__init__(parent)
        self.round_shadow = RoundShadow(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        _global_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(r'.wish\fonts\HYWH-85w Heavy.ttf'))[0]  
        
        self.wish_window = wish_window
        self.root_settings = root_settings
        self.dc_layout = QVBoxLayout(self)

        self.dc_header_layout = QHBoxLayout()  #
        title_label = '开发者指令' if _default_lang == 0 else 'Developer Command'
        self.dc_title_label = QLabel(title_label, self)
        self.dc_title_label.setFont(QFont(_global_font, 11))
        self.dc_close_button = QPushButton('', self)
        self.dc_close_button.setIcon(QIcon(r'.wish\assets\icon\close.png'))
        self.dc_close_button.setFont(QFont(_global_font, 12))
        self.dc_close_button.clicked.connect(self.close)
        self.dc_close_button.setFixedSize(30, 30)
        self.dc_close_button.setStyleSheet("""
            QPushButton:hover {
                border-radius: 5px;
                background-color: red;
                color: white; }""")
        self.dc_header_layout.addWidget(self.dc_title_label)
        self.dc_header_layout.addStretch(1)
        self.dc_header_layout.addWidget(self.dc_close_button)

        self.dc_table = QHBoxLayout()  # 

        self.command_input = QLineEdit(self)
        self.command_input.setFont(QFont(_global_font, 14))
        self.command_input.setPlaceholderText("请输入指令..." if _default_lang == 0 else "Enter command...")
        self.command_input.returnPressed.connect(self.execute_command)

        self.execute_button = QPushButton("✔", self)
        self.execute_button.setFont(QFont(_global_font, 14))
        self.execute_button.setFixedSize(40, 40)
        self.execute_button.clicked.connect(self.execute_command)
        
        self.dc_table.addWidget(self.command_input)
        self.dc_table.addWidget(self.execute_button)

        self.dc_layout.addLayout(self.dc_header_layout)  # 
        self.dc_layout.addLayout(self.dc_table)
        self.dc_layout.setContentsMargins(30, 25, 30, 25)

        self.setWindowTitle("祈愿 · 幸运观众开发者指令")
        self.setWindowIcon(QIcon(_iconpath))    
        self.setGeometry(300, 300, 400, 50)

    def execute_command(self):  # 解析指令
        command = self.command_input.text().strip()
        if not command:
            MessageBox.show_messagebox("[开发者指令] ⚠未输入指令。" if self.root_settings.LANGUAGE_INDEX == 0 else "[Developer Command] ⚠No command entered.")
            self.command_input.setFocus()
            self.command_input.selectAll()
            return
            
        if not command.startswith('/'):
            MessageBox.show_messagebox("[开发者指令] ⚠指令应以 '/' 开头。" if self.root_settings.LANGUAGE_INDEX == 0 else "[Developer Command] ⚠Command should start with '/'.")
            self.command_input.setFocus()
            self.command_input.selectAll()
            return
            
        try:
            parts = shlex.split(command[1:])
        except ValueError as e:
            MessageBox.show_messagebox(f"[开发者指令] ⚠解析指令时出错: {e}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] ⚠Error parsing command: {e}")
            return
            
        if not parts:
            MessageBox.show_messagebox("[开发者指令] ⚠'/' 后未输入有效指令。" if self.root_settings.LANGUAGE_INDEX == 0 else "[Developer Command] ⚠No valid command entered after '/'.")
            return

        cmd_name = parts[0]
        args = parts[1:]

        command_map = {
            # 退出命令
            'esc': lambda: self.wish_window.close(),
            'exit': lambda: self.wish_window.close(),
            'quit': lambda: self.wish_window.close(),
            'close': lambda: self.wish_window.close(),
            'kill': lambda: self.wish_window.close(),
            
            # 单抽命令
            'pick1': lambda: self.wish_window.pick_once(),
            'pickonce': lambda: self.wish_window.pick_once(),
            'p1': lambda: self.wish_window.pick_once(),
            
            # 十连命令
            'pick10': lambda: self.wish_window.pick_ten(),
            'pickten': lambda: self.wish_window.pick_ten(),
            'p10': lambda: self.wish_window.pick_ten(),
            
            # 自定义抽取命令
            'pick': self._handle_pick_command,
            'p': self._handle_pick_command,
            
            # 重置命令
            'reset': self._handle_reset_command,
            
            # 历史记录命令
            'history': self._handle_history_command
        }

        if cmd_name not in command_map:
            self._unknown_command(cmd_name)
            return

        try:
            command_map[cmd_name]()
            MessageBox.show_messagebox(f"[开发者指令] 执行指令: {cmd_name}，参数: {args}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] Executing command: {cmd_name} with arguments: {args}")
            self.command_input.clear()
        except Exception as e:
            MessageBox.show_messagebox(f"[开发者指令] ⚠执行指令时出错: {e}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] ⚠Error executing command: {e}")

    # 辅助方法
    def _handle_pick_command(self):
        """处理抽取命令"""
        args = self._get_current_args()
        try:
            if len(args) == 1:
                num = int(args[0])
                if num not in self.wish_window.supportable_numbers:
                    raise ValueError
                self.wish_window.pick_once(forced_number=num)
            elif len(args) == 10:
                num_list = [int(arg) for arg in args]
                if any(num not in self.wish_window.supportable_numbers for num in num_list):
                    raise ValueError
                self.wish_window.pick_ten(forced_numbers=num_list)
            else:
                MessageBox.show_messagebox(f"[开发者指令] ⚠只能抽取单个学号或十个学号: {args}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] ⚠You can only pick a single number or ten numbers: {args}")
                self.command_input.setFocus()
                self.command_input.selectAll()
        except ValueError:
            MessageBox.show_messagebox(f"[开发者指令] ⚠存在不支持的学号，请检查: {args[0]}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] ⚠Unsupported number exists: {args[0]}")
            self.command_input.setFocus()
            self.command_input.selectAll()

    def _handle_reset_command(self):
        """处理重置命令"""
        args = self._get_current_args()
        if not args or args[0] == 'all':
            self.wish_window.hide_newspaper()
            self.wish_window.clear_label()
            self.wish_window.reset_guarantee()
            self.wish_window.history_all = []
        elif args[0] in ['guarantee', 'gt']:
            self.wish_window.reset_guarantee()
        else:
            self._unknown_command('reset')

    def _handle_history_command(self):
        """处理历史记录命令"""
        args = self._get_current_args()
        if not args or args[0] in ['show']:
            self.wish_window.show_history()
        elif args[0] in ['clear']:
            self.wish_window.history_all = []
        else:
            self._unknown_command('history')

    def _unknown_command(self, cmd_name):
        """处理未知命令"""
        MessageBox.show_messagebox(f"[开发者指令] ⚠未知指令: {cmd_name}" if self.root_settings.LANGUAGE_INDEX == 0 else f"[Developer Command] ⚠Unknown command: {cmd_name}")
        self.command_input.setFocus()
        self.command_input.selectAll()

    def _get_current_args(self):
        """获取当前命令参数"""
        command = self.command_input.text().strip()
        parts = shlex.split(command[1:])
        return parts[1:] if len(parts) > 1 else []