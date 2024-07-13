import win32api
import win32con
import win32gui

# from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
# from PyQt5.QtGui import QIcon, QCursor


class AdvancedMenuEx():
    def __init__(self, menu_items):
        self.menu_items = menu_items

    def create_menu():
        """ 创建并返回一个上下文菜单。 """
        menu = win32gui.CreatePopupMenu()
        win32gui.AppendMenu(menu, win32con.MF_STRING, 1000, "选项 1")
        win32gui.AppendMenu(menu, win32con.MF_STRING, 1001, "选项 2")
        return menu

    def popup(self):
        """ 主函数，用于创建临时窗口和菜单，并处理用户的选择。 """
        hInstance = win32api.GetModuleHandle()
        className = 'MyInvisibleWindowClass'

        # 注册窗口类
        wndClass = win32gui.WNDCLASS()
        wndClass.lpfnWndProc = {win32con.WM_DESTROY: lambda hwnd, msg, wparam, lparam: 0}
        wndClass.hInstance = hInstance
        wndClass.lpszClassName = className
        win32gui.RegisterClass(wndClass)

        # 创建不可见窗口
        hwnd = win32gui.CreateWindow(className, 'Menu', 0, 0, 0, 0, 0, 0, 0, hInstance, None)

        try:
            menu = create_menu()
            x, y = win32api.GetCursorPos()

            # 显示菜单
            win32gui.SetForegroundWindow(hwnd)
            selected_option = win32gui.TrackPopupMenu(menu, win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY, x, y, 0, hwnd, None)
            win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

            # 检查用户的选择
            if selected_option:
                print(f"选中了菜单项: {selected_option}")
            else:
                print("没有选择任何菜单项")
        finally:
            # 清理资源
            win32gui.DestroyMenu(menu)
            win32gui.DestroyWindow(hwnd)
            win32gui.UnregisterClass(className, hInstance)



    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        self.loadMenuItems(contextMenu)
        # 在鼠标位置显示菜单
        action = contextMenu.exec_(QCursor.pos())
        if action:
            print(f"选择了 {action.text()}")
        else:
            print("没有选择任何菜单项")

    def loadMenuItems(self, contextMenu):
        for item in self.menu_items:
            if item == "SEPARATOR":
                contextMenu.addSeparator()
            else:
                if "icon" in item:
                    action = QAction(QIcon(item["icon"]), item["text"], self)
                else:
                    action = QAction(item["text"], self)
                if "callback" in item:
                    action.triggered.connect(item["callback"])
                if "enabled" in item:
                    action.setEnabled(item["enabled"])
                if "checkable" in item:
                    action.setCheckable(item["checkable"])
                contextMenu.addAction(action)

    def onActionClicked(self, checked=False):
        sender = self.sender()
        print(f"菜单项 {sender.text()} 被点击")


# if __name__ == '__main__':
#     menu_items = [
#         {"text": "普通选项", "callback": lambda: print("普通选项被点击")},
#         {"text": "带图标的选项", "icon": "logo.png",
#             "callback": lambda: print("带图标的选项被点击")},
#         "SEPARATOR",
#         {"text": "禁用选项", "enabled": False},
#         {"text": "复选框选项", "checkable": True,
#             "callback": lambda: print("复选框选项被点击")}
#     ]

#     ex = AdvancedMenuEx(menu_items)
#     ex.popup()


def create_menu():
    """ 创建并返回一个上下文菜单。 """
    menu = win32gui.CreatePopupMenu()
    win32gui.AppendMenu(menu, win32con.MF_STRING, 1000, "选项 1")
    win32gui.AppendMenu(menu, win32con.MF_STRING, 1001, "选项 2")
    return menu

def main():
    """ 主函数，用于创建临时窗口和菜单，并处理用户的选择。 """
    hInstance = win32api.GetModuleHandle()
    className = 'MyInvisibleWindowClass'

    # 注册窗口类
    wndClass = win32gui.WNDCLASS()
    wndClass.lpfnWndProc = {win32con.WM_DESTROY: lambda hwnd, msg, wparam, lparam: 0}
    wndClass.hInstance = hInstance
    wndClass.lpszClassName = className
    win32gui.RegisterClass(wndClass)

    # 创建不可见窗口
    hwnd = win32gui.CreateWindow(className, 'Menu', 0, 0, 0, 0, 0, 0, 0, hInstance, None)

    try:
        menu = create_menu()
        x, y = win32api.GetCursorPos()

        # 显示菜单
        win32gui.SetForegroundWindow(hwnd)
        selected_option = win32gui.TrackPopupMenu(menu, win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY, x, y, 0, hwnd, None)
        win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

        # 检查用户的选择
        if selected_option:
            print(f"选中了菜单项: {selected_option}")
        else:
            print("没有选择任何菜单项")
    finally:
        # 清理资源
        win32gui.DestroyMenu(menu)
        win32gui.DestroyWindow(hwnd)
        win32gui.UnregisterClass(className, hInstance)

if __name__ == "__main__":
    main()
