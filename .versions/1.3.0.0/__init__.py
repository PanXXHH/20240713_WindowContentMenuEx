from pathlib import Path
import sys
import importlib
# import datetime
import PySimpleGUI as sg
import libs.register as register
import libs.AdvancedMenuEx as AdvancedMenuEx
# from mysupport.PopupWindowGenerator._2 import PopupWindowGenerator
import utils
import yaml

with open('config.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

print(config)

# ***** 调试参数输入区 *****
# sys.argv.append("")
# sys.argv[1] = r"E:\工作台"
# *************************

# 检查命令行参数是否少于2个，是则退出
if len(sys.argv) < 2:
    exit(-1)

root_path = Path(sys.argv[1])

debug_mode = False
debug_mode = True
# 如果开启调试模式，将标准输出和标准错误输出重定向到 std.log 文件
if debug_mode:
    f = open(root_path / 'std.log', 'w')
    sys.stdout = f
    sys.stderr = f

smartdirectory_path = root_path / ".smart"
# 检查 smart 文件夹是否存在，不存在则退出
if not smartdirectory_path.exists() or smartdirectory_path.is_file():
    sg.popup_error("smart 文件夹不存在！请检查目录是否正确",font="微软雅黑")
    exit(-1)

# 将 smart 文件夹添加到系统路径
sys.path.append(str(smartdirectory_path))

targetfilename = '_contentmenuex.py'

abstf_path = smartdirectory_path / targetfilename

# 检查目标文件是否存在，不存在则退出
if not abstf_path.exists() or abstf_path.is_dir():
    sg.popup_error("_contentmenuex.py 文件不存在！请检查目录是否正确",font="微软雅黑")
    exit(-1)

# 注册 contentmenuex 模块
register.register(str(abstf_path), Path(__file__).parent / "regedit.yml")

# 导入 contentmenuex 模块
contentmenuex = importlib.import_module('_contentmenuex')




# 创建弹出式菜单
menu_items = []
for id, menuinfo in enumerate(contentmenuex.menu):
    name, func = menuinfo
    print(id, name, func)
    menu_items.append({"text": name, "callback": lambda
                      func=func, path=sys.argv[1]: func(path)})

menu_items.append({})
menu_items.append(
    {"text": "提交POST", "callback": lambda path=sys.argv[1]: utils.suggestions(path=path)})
menu_items.append({"text": "取消", "callback": lambda: ...})

AdvancedMenuEx.AdvancedMenuEx(menu_items).popup()
