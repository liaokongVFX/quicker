# -*- coding: utf-8 -*-
# Time    : 2021/2/16 15:37
# Author  : LiaoKong

import os
import ctypes
from ctypes.wintypes import *
import platform


class Everything(object):
    def __init__(self, max_query_num=20):
        dll_file = 'Everything32.dll'
        if platform.architecture()[0].startswith('64'):
            dll_file = 'Everything64.dll'
        self.everything_dll = ctypes.WinDLL(os.path.join(os.path.dirname(__file__), 'dll', dll_file))
        self.everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultFileNameW.argtypes = [DWORD]
        self.everything_dll.Everything_GetResultFileNameW.restype = ctypes.POINTER(ctypes.c_wchar)
        self.everything_dll.Everything_SetMax(max_query_num)

    def query(self, text):
        self.everything_dll.Everything_SetSearchW(ctypes.c_wchar_p(text))
        self.everything_dll.Everything_QueryW(True)
        num_results = self.everything_dll.Everything_GetNumResults()
        full_path = ctypes.create_unicode_buffer(500)
        results = []

        for i in range(num_results):
            self.everything_dll.Everything_GetResultFullPathNameW(i, full_path, 490)
            path = ctypes.wstring_at(full_path)
            results.append(path)

        return results


if __name__ == '__main__':
    e = Everything()
    print e.query('m.mov')
