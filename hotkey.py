# -*- coding: utf-8 -*-
# Time    : 2021/2/9 10:15
# Author  : LiaoKong
import sys
import ctypes
import ctypes.wintypes

from PySide2.QtCore import *

ALT = 1
CONTROL = 2
SHIFT = 4
WIN = 8
WM_HOTKEY = 786

mod_keys = {'ctrl': CONTROL, 'alt': ALT, 'shift': SHIFT}

# msdn.microsoft.com/en-us/library/dd375731
# http://www.kbdedit.com/manual/low_level_vk_list.html
code_by_vk = {
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
    '`': 0xC0,
}


class HotkeyThread(QThread):
    show_main_sign = Signal()
    shortcut_triggered = Signal(str)

    def __init__(self, key_map, parent=None):
        super(HotkeyThread, self).__init__(parent)
        self.key_map = key_map

    def run(self):
        user32 = ctypes.windll.user32
        param_map = {}
        try:
            param = 369
            for key in self.key_map:
                param += 1
                callback_name = self.key_map[key]
                keys = key.split('+')
                fk = 0
                if len(keys) > 1:
                    fk = sum([mod_keys[key.lower()] for key in keys[:-1]])
                vk = code_by_vk.get(keys[-1].lower())
                if not vk:
                    vk = ord(keys[-1])
                user32.RegisterHotKey(None, param, fk, vk)
                param_map[param] = callback_name
        except BaseException as e:
            sys.exit()
        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == WM_HOTKEY:
                    param = int(msg.wParam)
                    if param in param_map:
                        if not param_map[param]:  # main hotkey
                            self.show_main_sign.emit()
                        else:
                            self.shortcut_triggered.emit(param_map[param])
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, 1)
