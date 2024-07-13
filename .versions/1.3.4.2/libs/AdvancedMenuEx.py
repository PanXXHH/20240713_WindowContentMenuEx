import win32api
import win32con
import win32gui

class AdvancedMenuEx():
    def __init__(self, menu_items: list):
        """
        初始化AdvancedMenuEx类。

        :param menu_items: 包含菜单项的列表，每个菜单项是一个字典，包含'text'和'callback'键。
        """
        self.menu_items: list[dict] = menu_items
        self.index = 0  # 用于为每个菜单项分配唯一索引
        self.infos: dict[int, dict] = {}  # 存储菜单项信息的字典，以索引为键

    def create_menu(self):
        """
        创建并返回一个上下文菜单。

        :return: 创建的上下文菜单句柄。
        """
        menu = win32gui.CreatePopupMenu()  # 创建一个空的弹出菜单
        for menu_item in self.menu_items:
            self.index += 1
            self.infos[self.index] = menu_item  # 将菜单项信息存储在字典中
            if "text" not in menu_item:
                # 如果菜单项没有'text'键，添加一个分隔符
                win32gui.AppendMenu(menu, win32con.MF_SEPARATOR, 0, chr(0))
                continue
            # 添加一个普通的菜单项
            win32gui.AppendMenu(menu, win32con.MF_STRING, self.index, menu_item.get("text"))
        return menu

    def popup(self):
        """
        主函数，用于创建临时窗口和菜单，并处理用户的选择。
        """
        hInstance = win32api.GetModuleHandle()  # 获取当前模块的实例句柄
        className = 'MyInvisibleWindowClass'  # 定义窗口类名

        # 注册窗口类
        wndClass = win32gui.WNDCLASS()
        wndClass.lpfnWndProc = {win32con.WM_DESTROY: lambda hwnd, msg, wparam, lparam: 0}
        wndClass.hInstance = hInstance
        wndClass.lpszClassName = className
        win32gui.RegisterClass(wndClass)

        # 创建不可见窗口
        hwnd = win32gui.CreateWindow(className, 'Menu', 0, 0, 0, 0, 0, 0, 0, hInstance, None)

        try:
            if not hwnd:
                raise RuntimeError("Failed to create window")  # 如果窗口创建失败，抛出异常

            menu = self.create_menu()  # 创建菜单
            x, y = win32api.GetCursorPos()  # 获取当前鼠标位置

            # 将窗口设置为前台窗口
            win32gui.SetForegroundWindow(hwnd)
            # 显示弹出菜单并获取用户选择的菜单项ID
            selected_option = win32gui.TrackPopupMenu(
                menu, win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY, x, y, 0, hwnd, None)
            # 发送一个空消息，以确保菜单关闭
            win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

            if selected_option:
                # 执行用户选择的菜单项的回调函数
                self.infos[selected_option].get("callback", lambda: ...)()
        finally:
            # 清理资源
            win32gui.DestroyMenu(menu)  # 销毁菜单
            win32gui.DestroyWindow(hwnd)  # 销毁窗口
            win32gui.UnregisterClass(className, hInstance)  # 注销窗口类

# # 示例菜单项
# menu_items = [
#     {"text": "选项 1", "callback": lambda: print("选项 1 被选择")},
#     {"text": "选项 2", "callback": lambda: print("选项 2 被选择")},
#     {},
#     {"text": "选项 3", "callback": lambda: print("选项 3 被选择")},
# ]

# # 创建并显示菜单
# AdvancedMenuEx(menu_items).popup()
