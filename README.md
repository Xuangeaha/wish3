# 祈愿·幸运观众 3 (Wish3: Who's the Luckiest Dog?)

基于Qt框架的小型抽学号桌面应用程序。  

A Qt-based desktop gadget for randomly selecting student numbers.

**当前正式版：**`3.0` &emsp;&emsp;**当前开发版本：**`3.1-dev09.51-exp7`&emsp;&emsp;![Downloads](https://vsmarketplacebadges.dev/downloads/xuangeaha.wish3-whos-the-luckiest-dog.svg?&subject=全球下载量（次）)

## 开发中 Developing

### 祈愿 · 幸运观众 3.1：「心之捆绑」与「心之隔离」机制

    ·「心之捆绑」
        强制使两学号在两次连续祈愿中依次抽出。示例：“5-32 23-24”
        · 为保证机制公平，通过该方式祈愿获得的学号不计入保底。
        · 当存在重复学号时，写在前面的学号优先被捆绑。
            · 示例：设置“31-5 32-5”时，祈愿获得“5”后，下次祈愿将获得“31”.

    ·「心之隔离」
        限制两学号不得在两次连续祈愿中依次抽出。示例：“5|32 23|24”
        · 为保证机制公平，为满足该机制而进行强制插入的学号不计入保底。

    「心之捆绑」与「心之隔离」均可在「设置」窗口设置。以正确格式输入捆绑或隔离学号，点击“应用”按钮后，自下一次祈愿起即生效。
    
    · 该机制于「祈愿 · 幸运观众」开发版本3.1-dev09.51-exp后加入。

**Copyright © 2023-2024 XuangeAha(轩哥啊哈OvO)**

**All rights reserved. | MIT License**
