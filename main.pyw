"""
祈愿·幸运观众 3 (Wish3: Who's the Luckiest Dog?)

Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)
All rights reserved. | MIT License

"""


import sys
from WishWindow import WishWindow

from PyQt5.QtWidgets import QApplication

_short_ver = '3.1'
_ver = '3.1-dev09.5100-exp'
_vername = '早期开发'
_global_font = '汉仪文黑-85w'
_iconpath = r'wish.ico'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = WishWindow()
    root.show()
    app.exec_()
