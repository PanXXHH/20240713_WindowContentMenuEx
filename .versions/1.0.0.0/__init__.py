import sys
import os
import win32gui
from win32con import *
import importlib

debug = False
if debug:
    f = open('std.log', 'a')
    sys.stdout = f
    sys.stderr = f # redirect std err, if necessary
smartdirectory = ".smart\\"
# 判断smart文件夹是否存在，不存在退出
if not os.path.exists(smartdirectory):
    exit(-3)

sys.path.append(os.path.abspath(smartdirectory))

targetfilename = '_contentmenuex.py'
# 判断文件是否存在，不存在退出
abstf = os.path.join(smartdirectory, targetfilename)
if not os.path.exists(abstf):
    exit(-1)

contentmenuex = importlib.import_module('_contentmenuex')


def WndProc(hwnd, msg, wParam, lParam):
    # print(hwnd, msg, wParam, lParam)
    if msg == WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        win32gui.DrawText(hdc, 'GUI Python', len('GUI Python'),
                          rect, DT_SINGLELINE | DT_CENTER | DT_VCENTER)
        win32gui.EndPaint(hwnd, ps)
    if msg == WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)


wc = win32gui.WNDCLASS()
wc.hbrBackground = COLOR_BTNFACE + 1
wc.hCursor = win32gui.LoadCursor(0, IDI_APPLICATION)
wc.lpszClassName = "Python no Windows"
wc.lpfnWndProc = WndProc
reg = win32gui.RegisterClass(wc)
hwnd = win32gui.CreateWindow(reg, 'www.jb51.net - Python', WS_OVERLAPPEDWINDOW,
                             CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, 0, None)
menu = win32gui.CreatePopupMenu()
for id, menuinfo in zip(range(len(contentmenuex.menu)), contentmenuex.menu):
    name, func = menuinfo
    win32gui.AppendMenu(menu, MF_STRING, id+1, name)
win32gui.AppendMenu(menu, MF_SEPARATOR, -1, "")
win32gui.AppendMenu(menu, MF_STRING, -1, "取消")

flags = win32gui.TrackPopupMenu(menu, TPM_RETURNCMD, win32gui.GetCursorPos()[
    0], win32gui.GetCursorPos()[1], 0, hwnd, None)

if flags < 1:
    exit(flags)

for id, menuinfo in zip(range(len(contentmenuex.menu)), contentmenuex.menu):
    if flags == id+1:
        name, func = menuinfo
        func(sys.argv[1])
        break

exit(1)
