from abc import ABC, abstractmethod
import inspect

class CoreExport(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def default(self):
        pass

    def __setattr__(self, name, value):

        # 如果属性名以单个下划线开头，不处理
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        # 检查name是否全是大写，且value不是None
        if name.isupper() and value is not None:
            # 检查属性是否已经存在且不为None，若是，则抛出异常
            if hasattr(self, name) and getattr(self, name) is not None:
                raise ValueError(f"禁止修改常量 '{name}'.")

        # 对于其他情况，正常设置属性
        super().__setattr__(name, value)

    def __getattribute__(self, item):
        if item == '_' or item == '__':
            return super().__getattribute__(item)
        if len(item) > 2 and item[:2] == '__':
            return super().__getattribute__(item)
        if str(item)[0] == '_':
            if inspect.stack()[1][0].f_locals.get('self') != self:
                raise ValueError('该成员为受保护类型，禁止外部访问')

        return super().__getattribute__(item)