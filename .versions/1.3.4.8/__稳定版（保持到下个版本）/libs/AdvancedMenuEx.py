# from typing import Callable
import win32api
import win32con
import win32gui

class AdvancedMenuEx():
    def __init__(self, menu_items: list):
        self.menu_items: list[dict] = menu_items
        self.index = 0
        self.infos: dict[int, dict] = {}

    def create_menu(self):
        """ 创建并返回一个上下文菜单。 """
        menu = win32gui.CreatePopupMenu()
        for menu_item in self.menu_items:
            # 先加索引为了防止意外性重叠
            # print(menu_item)
            self.index += 1
            self.infos[self.index] = menu_item
            if "text" not in menu_item:
                win32gui.AppendMenu(menu, win32con.MF_SEPARATOR, 0, chr(0))
                continue
            win32gui.AppendMenu(menu, win32con.MF_STRING,
                                self.index, menu_item.get("text"))
        # win32gui.AppendMenu(menu, win32con.MF_STRING, 1001, "选项 2")
        return menu

    def popup(self):
        """ 主函数，用于创建临时窗口和菜单，并处理用户的选择。 """
        hInstance = win32api.GetModuleHandle()
        className = 'MyInvisibleWindowClass'

        # 注册窗口类
        wndClass = win32gui.WNDCLASS()
        wndClass.lpfnWndProc = {
            win32con.WM_DESTROY: lambda hwnd, msg, wparam, lparam: 0}
        wndClass.hInstance = hInstance
        wndClass.lpszClassName = className
        win32gui.RegisterClass(wndClass)

        # 创建不可见窗口
        hwnd = win32gui.CreateWindow(
            className, 'Menu', 0, 0, 0, 0, 0, 0, 0, hInstance, None)

        try:
            menu = self.create_menu()
            x, y = win32api.GetCursorPos()

            # 显示菜单
            win32gui.SetForegroundWindow(hwnd)
            selected_option = win32gui.TrackPopupMenu(
                menu, win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY, x, y, 0, hwnd, None)
            win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

            # 检查用户的选择
            # print(selected_option)
            if selected_option:
                self.infos[selected_option].get("callback", lambda: ...)()
        finally:
            # 清理资源
            win32gui.DestroyMenu(menu)
            win32gui.DestroyWindow(hwnd)
            win32gui.UnregisterClass(className, hInstance)

