"""
祈愿 · 幸运观众：异常崩溃处理

Copyright © 2025 XuangeAha(轩哥啊哈OvO)

"""

from PyQt5.QtWidgets import QMessageBox
import sys
import time


def handle_exception(exc_type, exc_value, exc_traceback):
    
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    from SettingsWindow import SettingsWindow
    SettingsWindow.show_messagebox(SettingsWindow, f"祈愿 · 幸运观众发生严重未知错误 ({time.asctime(time.localtime())})：\n\n\n        >>> {exc_type.__name__}: {exc_value}\n\n\n您可前往 VSMarketplace Q&A 或 Github 源代码仓库 Issues 栏目反馈问题。感谢您对祈愿 · 幸运观众作出的贡献。", lang=0, type=QMessageBox.Critical)
    
    sys.exit(1)
