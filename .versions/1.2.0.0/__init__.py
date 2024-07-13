from pathlib import Path
import sys
# import os
import importlib
import datetime
import PySimpleGUI as sg
import libs.register as register
# from mysupport.Pather.Pather3 import Pather as PathChain
import libs.AdvancedMenuEx as AdvancedMenuEx

# sys.argv.append("")
# sys.argv[1] = r"G:\Program Data\ONEDRIVE\987384390\OneDrive\新存储\PY-MYGOV\时区\财司时区"
# 检查命令行参数是否少于2个，是则退出
if len(sys.argv) < 2:
    exit(-1)


root_path = Path(sys.argv[1])

debug = False
# debug = True
# 如果开启调试模式，将标准输出和标准错误输出重定向到 std.log 文件
if debug:
    f = open(root_path / 'std.log', 'w')
    sys.stdout = f
    sys.stderr = f

smartdirectory_path = root_path / ".smart"
# 检查 smart 文件夹是否存在，不存在则退出
if not smartdirectory_path.exists() or smartdirectory_path.is_file():
    exit(-1)

# 将 smart 文件夹添加到系统路径
sys.path.append(str(smartdirectory_path))

targetfilename = '_contentmenuex.py'

abstf_path = smartdirectory_path / targetfilename

# 检查目标文件是否存在，不存在则退出
if not abstf_path.exists() or abstf_path.is_dir():
    exit(-1)

# 注册 contentmenuex 模块
register.register(str(abstf_path), Path(__file__).parent / "regedit.yml")

# 导入 contentmenuex 模块
contentmenuex = importlib.import_module('_contentmenuex')

# 获取 contentmenuex 需求公共库
if hasattr(contentmenuex, 'import_package'):
    import_package: dict = contentmenuex.import_package
    for key in import_package.keys():
        # 找看看能不能找到包，找不到要报错
        site_package_path = Path(__file__).parent / "Lib" / "site-packages"
        print(site_package_path)
        # 使用os.path.exists()检查路径是否存在
        if (site_package_path / str(key)).exists():
            # 使用os.path.isdir()检查路径是否为目录
            if (site_package_path / str(key)).is_dir():
                print("文件夹存在")
                # 将 smart 文件夹添加到系统路径
                sys.path.append(str(site_package_path))
                package = importlib.import_module(key)
                import_package[key] = package
            else:
                raise ValueError(f"Cannot find package '{key}'")
        else:
            raise ValueError(f"Cannot find package '{key}'")
    # print(import_package)


def suggestions():
    submit = sg.popup_get_text("提交内容", font="微软雅黑")
    with open(smartdirectory_path / 'suggestions.txt', 'a')as file:
        file.writelines("%s %s\n" %
                        (str(datetime.datetime.now()), submit))


# 创建弹出式菜单
menu_items = []
for id, menuinfo in enumerate(contentmenuex.menu):
    name, func = menuinfo
    print(id, name, func)
    menu_items.append({"text": name, "callback": lambda checked,
                      func=func, path=sys.argv[1]: func(path)})
    # menu_items.append({"text": name, "callback": lambda : func(sys.argv[1])})

# print(menu_items)
menu_items.append("SEPARATOR")
menu_items.append({"text": "提交建议", "callback": lambda: suggestions()})
menu_items.append({"text": "取消", "callback": lambda: ...})

AdvancedMenuEx.AdvancedMenuEx(menu_items).popup()
