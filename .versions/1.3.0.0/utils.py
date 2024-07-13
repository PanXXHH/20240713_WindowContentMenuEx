from pathlib import Path
from mysupport.PopupWindowGenerator._2 import PopupWindowGenerator
import datetime


def suggestions(path: str):
    path_path = Path(path)
    pwg = PopupWindowGenerator(title=f"Post", buttons=[
                               '确定', '取消'], esc_exit=True)
    pwg.add_input_element(str, "内容")
    event, values = pwg.popup(
        f"收件方：{path_path.name}(.postbox@service_path.*.wcmex)")

    # print(event, values)
    if not event or event == "取消":
        return

    content = str(values[0])

    if not content:
        pwg = PopupWindowGenerator().popup("内容不能为空！")
        raise Exception("内容不能为空！")

    postbox_path = path_path / ".postbox"
    postbox_path.mkdir(exist_ok=True)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 获取当前日期并格式化
    filename = postbox_path / f'{current_date}.txt'
    # print(filename)
    if filename.exists():
        pwg = PopupWindowGenerator().popup("发送消息太频繁，稍后重试！")
        raise Exception("发送消息太频繁，稍后重试！")

    with filename.open(mode="w",encoding="utf8") as file:
        file.write(content)

    PopupWindowGenerator().popup("邮件发送成功！")