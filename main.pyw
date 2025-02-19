"""
祈愿·幸运观众 3 (Wish3: Who's the Luckiest Dog?)

> “无论当下的境遇如何，属于幸运观众们的星空中将永远闪耀着你的位置。”
> "No matter the present, your place will forever shine in the starry sky of the luckiest ones."

Copyright © 2023-2025 XuangeAha(轩哥啊哈OvO)
All rights reserved. | MIT License

"""

from PyQt5.QtWidgets import QApplication
import sys

from WishWindow import WishWindow
from exceptionHandler import handle_exception


sys.excepthook = handle_exception


def run():
    app = QApplication(sys.argv)
    root = WishWindow()
    root.show()
    app.exec_()


if __name__ == '__main__':
    run()
