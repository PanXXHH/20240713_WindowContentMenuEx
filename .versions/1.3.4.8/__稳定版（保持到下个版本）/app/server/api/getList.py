from ... import core as Core
from ... import models as Model
from ... import utils as Utils


# 添加工作文件API

class Export(Core.CoreExport):
    def __init__(self) -> None:
        super().__init__()

    def default():
        return '123'