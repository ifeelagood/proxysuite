#!/usr/bin/python3

import imp,os

def __gather_all__(dir="plugins"):
    
    modules_lst = os.listdir(dir)
    
    modules_lst.remove('__init__.py')
    modules_lst.remove('spys_one.py')
    

    grabbed = []
    
    for module_name in modules_lst:
        if module_name.split('.')[-1] == 'py':
            m = imp.load_source('module', dir + os.sep + module_name)
            g = m.Grabber()
            grabbed += g.grab_all()
    
    return grabbed        