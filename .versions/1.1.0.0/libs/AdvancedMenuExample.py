import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QIcon, QCursor

class AdvancedMenuExample(QMainWindow):
    def __init__(self, menu_items):
        self.app = QApplication([])
        super().__init__()
        self.menu_items = menu_items

    def popup(self):
        self.contextMenuEvent(None)

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
#         {"text": "带图标的选项", "icon": "logo.png", "callback": lambda: print("带图标的选项被点击")},
#         "SEPARATOR",
#         {"text": "禁用选项", "enabled": False},
#         {"text": "复选框选项", "checkable": True, "callback": lambda: print("复选框选项被点击")}
#     ]

#     ex = AdvancedMenuExample(menu_items)
#     ex.popup()