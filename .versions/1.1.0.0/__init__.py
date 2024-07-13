#!/usr/bin/env python
# coding=utf-8

import sys
import os
import win32gui
from win32con import *
import importlib
import datetime
import PySimpleGUI as sg
import libs.register as register
from ruamel.yaml import YAML
from mysupport.Pather.Pather3 import Pather
import libs.AdvancedMenuExample as AdvancedMenuExample


sys.argv.append("")
sys.argv[1] = r"G:\Program Data\ONEDRIVE\MY\OneDrive - Radomil Deanne\MYCLOUDDRIVE\CLOUD_MYAPPS\WindowContentMenuEx(MYTOOL)\.sandbox\.textbox"
# 检查命令行参数是否少于2个，是则退出
if len(sys.argv) < 2:
    exit(-1)

root_pather = Pather(sys.argv[1])
print("1", sys.argv[1], root_pather)
debug = False
# debug = True
# 如果开启调试模式，将标准输出和标准错误输出重定向到 std.log 文件
if debug:
    f = open(root_pather('std.log').str(), 'w')
    sys.stdout = f
    sys.stderr = f

smartdirectory = root_pather(".smart\\")
# 检查 smart 文件夹是否存在，不存在则退出
if not smartdirectory.exists():
    exit(-1)

# 将 smart 文件夹添加到系统路径
sys.path.append(smartdirectory.str())

targetfilename = '_contentmenuex.py'
# 检查目标文件是否存在，不存在则退出
abstf = smartdirectory(targetfilename)
if not abstf.exists():
    exit(-1)

# 注册 contentmenuex 模块
register.register(abstf.str(), Pather(__file__).dirname()("regedit.yml").str())

# 导入 contentmenuex 模块
contentmenuex = importlib.import_module('_contentmenuex')

# 获取 contentmenuex 需求公共库
if hasattr(contentmenuex, 'import_package'):
    import_package: dict = contentmenuex.import_package
    for key in import_package.keys():
        # 找看看能不能找到包，找不到要报错
        site_package_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "Lib", "site-packages")
        print(site_package_path)
        # 使用os.path.exists()检查路径是否存在
        if os.path.exists(os.path.join(site_package_path, key)):
            # 使用os.path.isdir()检查路径是否为目录
            if os.path.isdir(os.path.join(site_package_path, key)):
                print("文件夹存在")
                # 将 smart 文件夹添加到系统路径
                sys.path.append(site_package_path)
                package = importlib.import_module(key)
                import_package[key] = package
            else:
                raise ValueError(f"Cannot find package '{key}'")
        else:
            raise ValueError(f"Cannot find package '{key}'")
    print(import_package)


def WndProc(hwnd, msg, wParam, lParam):
    # 处理窗口消息
    if msg == WM_PAINT:
        # 绘制窗口
        hdc, ps = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        win32gui.DrawText(hdc, 'GUI Python', len('GUI Python'),
                          rect, DT_SINGLELINE | DT_CENTER | DT_VCENTER)
        win32gui.EndPaint(hwnd, ps)
    if msg == WM_DESTROY:
        # 如果窗口被销毁，发送退出消息
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


# 定义窗口类
wc = win32gui.WNDCLASS()
wc.hbrBackground = COLOR_BTNFACE + 1
wc.hCursor = win32gui.LoadCursor(0, IDI_APPLICATION)
wc.lpszClassName = "Python no Windows"
wc.lpfnWndProc = WndProc

# 注册窗口类并创建窗口
reg = win32gui.RegisterClass(wc)
hwnd = win32gui.CreateWindow(reg, 'www.jb51.net - Python', WS_OVERLAPPEDWINDOW,
                             CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, 0, None)

# 创建弹出式菜单
menu = win32gui.CreatePopupMenu()
menu_items = []
for id, menuinfo in enumerate(contentmenuex.menu):
    name, func = menuinfo
    print(name,func)
    menu_items.append({"text": name, "callback": lambda : func(sys.argv[1])})
    win32gui.AppendMenu(menu, MF_STRING, id+1, name)

menu_items.append("SEPARATOR")
menu_items.append({"text": "提交建议", "callback": None})
menu_items.append({"text": "取消", "callback": None})
# win32gui.AppendMenu(menu, MF_SEPARATOR, -1, "")
# win32gui.AppendMenu(menu, MF_STRING, -2, "提交建议")
# win32gui.AppendMenu(menu, MF_STRING, -1, "取消")

AdvancedMenuExample.AdvancedMenuExample(menu_items).popup()


# # 显示弹出式菜单并获取选中的菜单项
# flags = win32gui.TrackPopupMenu(menu, TPM_RETURNCMD, win32gui.GetCursorPos()[
#     0], win32gui.GetCursorPos()[1], 0, hwnd, None)

# 处理选中的菜单项
# if flags < 1:
#     if flags == -1:
#         # 如果选择 "取消"，则不执行任何操作
#         ...
#     elif flags == -2:
#         # 如果选择 "提交建议"，则弹出输入框获取用户输入，并将内容追加到 suggestions.txt 文件
#         submit = sg.popup_get_text("提交内容", font="微软雅黑")
#         with open(smartdirectory('suggestions.txt').str(), 'a')as file:
#             file.writelines("%s %s\n" %
#                             (str(datetime.datetime.now()), submit))
#     exit(flags)

# 遍历菜单项并执行相应的函数
# for id, menuinfo in enumerate(contentmenuex.menu):
#     if flags == id+1:
#         name, func = menuinfo
#         func(sys.argv[1])
#         break

# 程序正常退出
exit(1)
