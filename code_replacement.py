#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import __main__
from ctypes import *

from sys import _getframe


BYTES_HEADER_SIZE = 32
CALL_BYTECODE = b'\x01\x00d\x00\x83\x00S\x00'
    # POP_TOP
    # LOAD_CONST 0
    # CALL_FUNCTION 0
    # RETURN_VALUE


def get_main_frame():
    frame = sys._getframe()
    while frame.f_back is not None:
        frame = frame.f_back
    return frame


def replace_main_bytecode(new_code):

    frame = get_main_frame()

    offset = BYTES_HEADER_SIZE + frame.f_lasti

    buffer = (ctypes.c_char * len(CALL_BYTECODE))
    target_data = buffer.from_address(
        id(frame.f_code.co_code) + offset
    )

    target_data[:] = CALL_BYTECODE

    constants = frame.f_code.co_consts
    ctypes.cast(id(constants), ctypes.POINTER(ctypes.py_object))[3] = new_code

from ctypes import *
from types import *
from code import *
from sys import *
from sys import _getframe

def overwrite(code, callable):
    def wrapper():
        locals = _getframe(1).f_locals # get the frame's locals
        return callable(*locals['args'], **locals['kwargs'])
    pythonapi.Py_IncRef(py_object(wrapper))
    if isinstance(code, FunctionType):
        code = code.__code__
    array = (c_char*5).from_address(id(code.co_code) + 32)
    array[:] = b'd\0\x83\0S' # load constant 0, call function, return
    cast(id(code.co_consts), POINTER(py_object))[3] = wrapper # overwrite the first thing in the tuple with a wrapper
    cast(id(code), POINTER(c_char))[24] = 2 # co_nlocals
    cast(id(code), POINTER(c_char))[32] = cast(id(code), POINTER(c_char))[32][0] | 12 # tinker with flags for *args and **kwargs
    varnames = ('args', 'kwargs')
    pythonapi.Py_IncRef(py_object(varnames))
    cast(id(code), POINTER(py_object))[8] = varnames
