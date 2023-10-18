# Mouse Free

> 释放鼠标，释放生产力

使用键盘操纵鼠标，减少键盘与鼠标的切换，提升效率。




## 特性

1. 快捷键唤醒软件，弹出幕布覆盖屏幕，幕布上展示标识符，
   1. 快捷键 ctrl + alt + space 弹出幕布，标识整个屏幕，使用英文字符 AA-ZZ 作为标识符。
   2. 快捷键 ctrl + alt + shift 弹出幕布，标识鼠标附近屏幕，使用英文字符 A-Z 作为标识符。
2. 幕布展示状态下，键盘输入标识符，鼠标移动到标识符所在位置。
3. 幕布弹出5秒后自动隐藏，或输入 ECS 后幕布主动隐藏，或执行任意有效操作后幕布主动隐藏。
4. 快捷键 ctrl + alt + q 退出软件。
5. 鼠标模拟
   1. 幕布展示状态下，快捷键 ctrl + alt + enter 模拟鼠标左键单击。
   2. 幕布展示状态下，快捷键 ctrl + alt + +（加号） 模拟鼠标左键双击。
   3. 幕布展示状态下，快捷键 ctrl + alt + - （减号）模拟鼠标右键单击。

6. 快捷键 ctrl + alt + 0 切换屏幕后弹出幕布，支持双屏幕（扩展屏）。
7. 快捷键 ctrl + alt + up（向上箭头） 弹出幕布，展示当前软件的快捷键。
8. 上述快捷键与时间参数均可自定义配置。




## 约束

1. 目前仅支持 Windows。
2. 已验证环境 Windows 10，Windows 11。
3. 部分逻辑依赖 windows api，使用 pywinauto 和 pygetwindow。




## 示例

快捷键 ctrl + alt + space 弹出幕布，标识整个屏幕，使用英文字符 AA-ZZ 作为标识符。

键盘输入标识符，鼠标移动到标识符所在位置。


![image](https://github.com/gdeveloping/mouse-free/assets/103371228/7fb519e0-2dd1-46a7-8f81-5a09cb3ed7e1)



## 开发环境

1. Windows 11
2. Python 3.10
3. VS Code



## 生成可执行文件命令

```powershell
pyinstaller.exe -F -n mouse-free-v0.1  --add-data="src\mouse-free.properties;." --add-data="src\hotkey.json;."  .\src\mouse-free-explore.py
```




## 路线图

- [x] 标识整个屏幕，键盘控制鼠标移动到屏幕指定位置。
- [x] 快捷键唤醒软件，默认处于沉睡状态。
- [x] 键盘控制鼠标左键单击。
- [x] 延迟隐藏窗口，使用线程池管理任务。
- [x] 标识鼠标附近屏幕，提升标识精确度。
- [x] 支持双屏幕。
- [x] 支持鼠标右键单击，左键双击。
- [x] 支持读取配置文件。
- [x] 支持展示当前使用软件（桌面顶层的软件）的快捷键
- [ ] 支持展示主流软件的快捷键
- [ ] 精简可执行文件大小
- [ ] 美化幕布 UI
- [ ] 支持 MacOS

* More ...



## License

LGPL



