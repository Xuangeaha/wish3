"""
祈愿·幸运观众 3 (Wish3: Who's the Luckiest Dog?)

Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)
All rights reserved. | MIT License

"""

import sys
from WishWindow import WishWindow

from PyQt5.QtWidgets import QApplication


def run():
    app = QApplication(sys.argv)
    root = WishWindow()
    root.show()
    app.exec_()


if __name__ == '__main__':
    run()
