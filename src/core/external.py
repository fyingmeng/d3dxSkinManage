# -*- coding: utf-8 -*-

import core

import threading
import subprocess

from . import env

import win32api

def is_main_thread(*args, **kwds) -> bool:
    return threading.current_thread() is threading.main_thread()


def x7z(from_file: str, to_path: str):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL
    command = (env.file.local.t7z, 'x', '-y', f'-o{to_path}', from_file)
    task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=env.base.cwd)
    task.wait()


def a7z(from_file: str, to_path: str):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL
    command = (env.file.local.t7z, 'a', '-t7z', to_path, from_file)
    task = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, cwd=env.base.cwd)
    task.wait()


def view_file(path: str):
    file = core.env.configuration.view_explorer_path
    rule = core.env.configuration.view_file_rule
    argument = rule.replace("{path}", path)
    win32api.ShellExecute(0, "open", file, argument, None, 1)


def view_directory(path: str):
    file = core.env.configuration.view_explorer_path
    rule = core.env.configuration.view_directory_rule
    argument = rule.replace("{path}", path)
    win32api.ShellExecute(0, "open", file, argument, None, 1)
