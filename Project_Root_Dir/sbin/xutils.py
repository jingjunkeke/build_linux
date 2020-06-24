#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import inspect
import subprocess

this_file = lambda: inspect.stack()[1][1]
this_line = lambda: inspect.stack()[1][2]
this_function = lambda: inspect.stack()[1][3]

this_abspath = lambda f:os.path.abspath(f)
this_dirname = lambda f:os.path.dirname(os.path.abspath(f))


import imp
import os

#imp.load_source(name, path)
#imp.load_compiled(name, path)

def instance_from_file(filepath, classname, *args, **kwargs):    
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, classname):
        return getattr(py_mod, classname)(*args, **kwargs)

    return None

def attribute_from_file(filepath, attrname):
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, attrname):
        return getattr(py_mod, attrname)

    return None

def module_from_file(filepath, attrname):
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        return imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        return imp.load_compiled(mod_name, filepath)
    else:
        return None

def shell_cmd(cmd_line, echo=True, shell=True, encoding='utf-8'):
    try:
        if echo:
            print(cmd_line)
            cp = subprocess.run(cmd_line, shell=shell, encoding=encoding)
        else:
            cp = subprocess.run(cmd_line, shell=shell, encoding=encoding)
        return cp.returncode
    except:
        raise SystemError('Invalid input command line')


if __name__ == '__main__':
    def fun():
       print(f"file: {this_file()}, line: {this_line()}, function: {this_function()}")

    fun()

    print(this_line())
    print(this_abspath(__file__))
    print(this_dirname(__file__))

    print(this_line())
    x = instance_from_file('../base/xpath.py', 'xPath', 'abc.efg.hij')
    print(dir(x))
    print(x.name)
    print(x.path)

    print(this_line())
    y = attribute_from_file('../base/xpath.py', 'xPath')
    print(dir(y))





