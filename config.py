"""
祈愿 · 幸运观众：全局变量

Copyright © 2024-2025 XuangeAha(轩哥啊哈OvO)

"""

_ver_short: str = '3.4.5'  # 短版本号
_ver: str = '3.4.5'  # 版本号
_ver_type: str = '正式版'  # 版本类型

_morning_newspaper: str = '感谢 2,400+ 次下载！'  # 晨报

_default_lang: int = 0  # 默认语言
_iconpath: str = r'wish.ico'  # 图标路径

_is_special_wish_on: bool = True  # 是否启用特殊祈愿模式
_is_debug_on: bool = True  # 是否启用调试模式
_is_profilephotoupdatewindow_shown: bool = False  # 是否显示头像更新窗口

_base_numbers: list = list(range(1, 42))  # 默认基础学号

# 保留了学号命名空间，但默认无法在祈愿中获得的学号
# “无论当下的境遇如何，属于幸运观众们的星空中将永远闪耀着你的位置。”
# "No matter the present, your place will forever shine in the starry sky of the luckiest ones."
_EVER_excluded_numbers: list = [13, 18]  

