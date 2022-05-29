#!/usr/bin/python3

import imp,os, threading

def __gather_all__(dir="plugins"):
    
    global grabbed
    grabbed = []
    
    modules_lst = os.listdir(dir)
    
    modules_lst.remove('__init__.py')
    modules_lst.remove('spys_one.py')
    

    threads = []
    
    for module_name in modules_lst:
        if module_name.split('.')[-1] == 'py':
            m = imp.load_source('module', dir + os.sep + module_name)
            x = threading.Thread(target=worker, args=(m,))
            threads.append(x)

    for x in threads:
        x.start()
        
    for x in threads:
        x.join()
    
    return grabbed


def worker(m):
    global grabbed
    g = m.Grabber()
    thread_grabbed = g.grab_all()
    grabbed += thread_grabbed