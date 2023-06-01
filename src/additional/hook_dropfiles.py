# -*- coding: utf-8 -*-

# std
import os
import threading

# project
import core

# self
from . import add_mod
from . import add_preview


rule_single = [
    (['.png', '.jpg'], add_preview.add_preview, False),
    (['.zip', '.rar', '.7z'], add_mod.AddMods, True)
]


def check_for_login() -> bool:
    return isinstance(core.environment.user.userName, str)


def hook_dropfiles(items: list):
    try:
        if not check_for_login():
            core.UI.Messagebox.showerror(title='未登录错误', message='必须先登录一个用户\n才能使用文件拖入功能')
            return

        lst = []

        for item in items:
            try:
                try: content = item.decode('utf-8')
                except Exception: content = item.decode('gb18030')
                lst.append(content)
            except Exception:
                core.UI.Messagebox.showerror(title='编码不可解', message='无法解码消息内容\n请检查系统编码是否为 utf-8 或 gb18030')
                return

        if len(lst) <= 0:
            ...

        elif len(lst) == 1:
            bin_dropfiles_single(lst.pop())

        else:
            bin_dropfiles_multiple(lst)

    except Exception:
        core.UI.Messagebox.showerror(title='触发器异常', message='hook 异常 / 任务冲突\n请稍后重试')


def __exec_call(func_, async_, arg_):
        if async_: threading.Thread(None, func_, 'hookTask', (arg_, ), daemon=True).start()
        else: func_(arg_)


def bin_dropfiles_single(content):
    if os.path.isfile(content):
        basename = os.path.basename(content)

        suffix = basename[basename.rfind('.'):]

        for rule in rule_single:
            accept_, func_, async_ = rule

            if suffix in accept_:
                __exec_call(func_, async_, content)
                return

        else:
            core.UI.Messagebox.showerror(title='不支持的文件类型', message='没有处理该文件类型的触发器')


    elif os.path.isdir(content):
        core.UI.Messagebox.showerror(title='无法处理', message='无法处理文件夹')
        return


    else:
        core.UI.Messagebox.showerror(title='无法处理', message='未知目标类型或路径不存在')
        return


def bin_dropfiles_multiple(content):
    core.UI.Messagebox.showerror(title='无法处理', message='无法一次性处理多个文件\n请将文件分别导入')
    return