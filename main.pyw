"""
祈愿 · 幸运观众 3 (Wish3: Who's the Luckiest Dog?)

> “无论当下的境遇如何，属于幸运观众们的星空中将永远闪耀着你的位置。”
> "No matter the present, your place will forever shine in the starry sky of the luckiest ones."

Copyright © 2023-2025 XuangeAha(轩哥啊哈OvO/卡猫kat)
MIT License | All rights reserved.

"""

from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import time

from WishWindow import WishWindow

def handle_exception(exc_type, exc_value, exc_traceback):
    
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    from SettingsWindow import SettingsWindow
    SettingsWindow.show_dialoguebox(SettingsWindow, f"祈愿 · 幸运观众发生严重未知错误 ({time.asctime(time.localtime())})：\n\n\n        >>> {exc_type.__name__}: {exc_value}\n\n\n您可前往 VSMarketplace Q&A 或 Github 源代码仓库 Issues 栏目反馈问题。感谢您对祈愿 · 幸运观众作出的贡献。", lang=0, type=QMessageBox.Critical)
    
    sys.exit(1)

sys.excepthook = handle_exception


def run():
    app = QApplication(sys.argv)
    
    root = WishWindow()
    root.show()

    app.exec_()


if __name__ == '__main__':
    run()

