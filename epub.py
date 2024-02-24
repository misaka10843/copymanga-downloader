import os
import platform
import random
import smtplib
import subprocess
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from rich import print as print
from rich.prompt import Prompt, Confirm

import config


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def epub_transformer(path: str, name: str, chapter: str) -> None:
    """
    将下载好的图片转化为epub待发送

    :param path: 漫画存放的根地址
    :param name: 漫画的名称
    :param chapter: 漫画的章节
    :return: 空
    """
    # 定义命令和参数
    # command = SETTINGS["kcc_cmd"]
    arguments = ["-o", f'{path}/{name}/{chapter}/{name} {chapter}.epub', "-t", f"{name} {chapter}",
                 f'{path}/{name}/{chapter}']
    command = config.SETTINGS["kcc_cmd"].split(" ") + arguments
    subprocess.run(command, shell=True, capture_output=True, text=True)


def mailtest(sender: str, passwd: str, receiver: str, smtp_address: str, message: str) -> bool:
    """
    用于测试邮件是否可用

    :param sender:
    :param passwd:
    :param receiver:
    :param smtp_address:
    :param message:
    :return: 发送成功返回 True, 如果发送失败会返回 False
    """
    try:
        my_sender = sender
        my_pass = passwd
        my_user = receiver

        msg = MIMEMultipart()

        msg['From'] = sender

        file = MIMEBase('application', 'octet-stream')
        file.add_header('Content-Disposition', 'attachment', filename=f"{message}.txt")
        file.set_payload(message.encode())
        encoders.encode_base64(file)
        msg.attach(file)
        msg['From'] = Header(my_sender)

        server = smtplib.SMTP_SSL(smtp_address, 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()

    except Exception as e:
        return False
    return True


def mail(fd) -> bool:
    """
    发送邮件函数

    :param fd: io文件句柄
    :return: 发送成功为真，否则为假
    """
    try:
        message = MIMEMultipart()
        file = MIMEBase('application', 'octet-stream')
        file.add_header('Content-Disposition', 'attachment', filename=fd.name.split("/")[-1])
        file.set_payload(fd.read())
        encoders.encode_base64(file)
        message.attach(file)
        message['From'] = Header(config.SETTINGS["email_address"])

        server = smtplib.SMTP_SSL(config.SETTINGS["email_smtp_address"], 465)
        server.login(config.SETTINGS["email_address"], config.SETTINGS["email_passwd"])
        server.sendmail(config.SETTINGS["email_address"], config.SETTINGS["kindle_address"], message.as_string())
        server.quit()

    except Exception as e:
        return False
    return True


def set_kindle_config() -> None:
    """
    发送到kindle的设置

    :return: 空
    """
    system = platform.system()
    path = os.path.split(os.path.realpath(__file__))[0]
    while not config.SETTINGS['kcc_cmd']:
        if system == "Windows":
            tmp = Prompt.ask(
                "请输入kcc_c2e路径[italic yellow](建议先查看配置教程 https://www.pursuecode.cn/archives/1705162565893，默认为copymanga-downloader目录)[/]",
                default=path) + "/kcc_c2e.exe"
        else:
            tmp = Prompt.ask(
                "请输入kcc_c2e路径[italic yellow](建议先查看配置教程 https://www.pursuecode.cn/archives/1705162565893,默认为copymanga-downloader目录)[/]",
                default=path) + "/kcc_c2e"
        if is_contains_chinese(tmp):
            print("[bold yellow]kcc_c2e路径请不要包含中文[/]")
            continue

        if os.path.exists(tmp):
            devices = "K1, K2, K34, K578, KDX, KPW, KPW5, KV, KO, K11, KS, KoMT, KoG, KoGHD, KoA, KoAHD, KoAH2O, KoAO, KoN, KoC, KoL, KoF, KoS, KoE"
            deviceset = set(devices.split(", "))
            while True:
                device = Prompt.ask(f"请输入kcc设备参数, 支持的设备有[italic yellow]{devices}[/]", default=False)
                device = device.strip()
                if device not in deviceset:
                    print("[bold red]设备不存在，请重新输入[/]")
                else:
                    break
            config.SETTINGS["kcc_cmd"] = f"{tmp} -p {device} -f EPUB"
            break
        else:
            print("[bold red]kcc_c2e不存在，请确认程序名称是否为kcc_c2e或是否安装kcc_c2e并且路径不含中文[/]")

    check = Confirm.ask("是否需要发送验证码到kindle验证", default=False)
    while True:
        email_address = Prompt.ask("请输入邮箱smtp账号[italic yellow](建议查看配置教程)[/]")
        email_passwd = Prompt.ask("请输入邮箱smtp密码")
        email_smtp_address = Prompt.ask("请输入邮箱smtp的地址")
        kindle_address = Prompt.ask(
            "请输入kindle推送邮件地址[italic yellow](如twoonefour_ABCDQA@kindle.com，具体请查看amazon设置)[/]")
        # email_address = "489643427@qq.com"
        # email_passwd = "xulsahtupltibjbh"
        # email_smtp_address = "smtp.qq.com"
        # kindle_address = "lys214412_uoeyap@kindle.com"
        if check:
            code = str(random.randint(100000, 999999))
            if mailtest(email_address, email_passwd, kindle_address, email_smtp_address, code):
                if code == Prompt.ask("请输入kindle上显示的验证码"):
                    print("[bold green]验证码正确，验证成功[/]")
                    break
                else:
                    print("[bold red]验证码错误，请重新输入配置[/]")
        else:
            break
    config.SETTINGS["email_address"] = email_address
    config.SETTINGS["email_passwd"] = email_passwd
    config.SETTINGS["kindle_address"] = kindle_address
    config.SETTINGS["email_smtp_address"] = email_smtp_address


def epub_transformerhelper(download_path, manga_name, chapter_name) -> None:
    """
    辅助函数，用于转换epub

    :param download_path:
    :param manga_name:
    :param chapter_name:
    :return:
    """
    if config.SETTINGS["send_to_kindle"]:
        if not os.path.exists(f'{download_path}/{manga_name}/{chapter_name}/{manga_name} {chapter_name}.epub'):
            epub_transformer(path=download_path, name=manga_name, chapter=chapter_name)
        with open(f'{download_path}/{manga_name}/{chapter_name}/{manga_name} {chapter_name}.epub', "rb") as f:
            mail(f)
