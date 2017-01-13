# -*- coding:utf-8 -*-  
from robot.libraries.Remote import Remote

class remote_run_key(object):
    
    def __init__(self):
        pass

    def remote_run_keyword(self,uri,name,*args):
        '''可以使用这个关键字在远程机上运行远程机的关键字。
            uri=http://192.168.7.108:8270   远程机的IP和端口。
            name=keyword   在远程机上运行的关键字。
            *args=args   关键字参数，可以是多个，用括号括起来。
            你可以在suit的添加全局变量，定义uri。
        '''
        client=Remote(uri)
        client.run_keyword(name=name,args=args,kwargs=False)