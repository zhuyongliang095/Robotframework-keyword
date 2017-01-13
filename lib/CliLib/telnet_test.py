# -*- coding:utf-8 -*-  
import telnetlib,time,sys
from AutomatedLib.lib.pub_lib import _unicode_to_utf,ExpectError,_searchchar
from AutomatedLib.configure import dut_user,dut_passwd,ros_user,ros_passwd

class telnet_test:
    def __init__(self):
        pass
    
    def telnet_run(self,host='',commands='',expect=None,searchchar=None,timeout=None,username=dut_user,passwd=dut_passwd):
        """
        telnet a dut and exec command,command will split by ';'.
        searchchar is the expect string,when expect=1,the result should contain the searchchar
        eg:
        | telnet_run | 192.168.2.132 | con t;in ge3/0;no ip add;show inter ge3/0 | 1 | search | admin | admin |
        when an error happend in cmd,such as '%unknown command',the program will drop an error
        if have show command in commands ,search result of show command;else search command have error or not
        """
        host=_unicode_to_utf(host)
        commands=_unicode_to_utf(commands)
        expect=_unicode_to_utf(expect)
        searchchar=_unicode_to_utf(searchchar)
        timeout=_unicode_to_utf(timeout)
        username=_unicode_to_utf(username)
        passwd=_unicode_to_utf(passwd)
        cmds=['enable']
        cmds+=commands.split(';')
        msgs=[]

        print("run keyword:%s *****************  host=%s"%(sys._getframe().f_code.co_name,host))
        tl=telnetlib.Telnet(host,23,10)
        tl.read_until("Username:")
        tl.write(username+'\n')
        tl.read_until("Password:")
        tl.write(passwd+'\n')
        tl.read_until('>')

        for cmd in cmds:
            if 'reboot' in cmd :
                tl.write('%s\n' % cmd)
                msg=tl.read_until('y/n')
                tl.write('y\n')
            else:
                if 'show' in cmd :
                    if timeout!=None and timeout!='None' and timeout!= '':
                        for i in range(int(timeout)):
                            try:
                                tl.write('%s\n' % cmd)
                                show_msg=tl.read_until('#')
                                print("%s"%show_msg)
                                #msgs.append(show_msg)
                                return _searchchar(searchchar,show_msg,expect,'show')
                            except ExpectError as e :
                                if i+1 == int(timeout):
                                    #msgs=' '.join(msgs)
                                    #print("%s"%msgs)
                                    raise ExpectError("search times %d error :%s"%(int(timeout),e))
                                else:
                                    print("search times %d error :%s"%(i,e))
                                    time.sleep(1)
                    else:
                        tl.write('%s\n' % cmd)
                        show_msg=tl.read_until('#')
                        msgs.append(show_msg)
                        try:
                            print("%s"%show_msg)
                            return _searchchar(searchchar,show_msg,expect,'show')
                        except ExpectError as e:
                            print("%s"%' '.join(msgs))
                            raise ExpectError("%s"%e)
                else :
                    tl.write('%s\n' % cmd)
                    msg=tl.read_until('#')
                    msgs.append(msg)
        msgs=' '.join(msgs)
        print("%s"%msgs)
        tl.close()

        #_searchchar(None,msgs,expect)
        if 'show_msg' not in locals().keys() :
            _searchchar(None,msgs,expect)


    def telnet_ros_run(self,host='',commands='',expect=None,searchchar=None,username=ros_user,passwd=ros_passwd):
        host=_unicode_to_utf(host)
        commands=_unicode_to_utf(commands)
        expect=_unicode_to_utf(expect)
        searchchar=_unicode_to_utf(searchchar)
        username=_unicode_to_utf(username)
        passwd=_unicode_to_utf(passwd)
        print("run keyword:%s    *****************   host=%s"%(sys._getframe().f_code.co_name,host))
        tl=telnetlib.Telnet(host,23,10)
        tl.read_until("Login:")
        tl.write(username+'\r\n')
        tl.read_until("Password:")
        tl.write(passwd+'\r\n')
        tl.read_until('>')
        cmds=commands.split(';')
        msgs=[]
        print("%s"%cmds)
        for cmd in cmds:
            print("cmd=%s"%cmd)
            tl.write(cmd+'\r\n')
            if 'print' in cmd :
                show_msg=tl.read_until('>',10)
                msgs.append(show_msg)
            else :
                msg=tl.read_until('>',10)
                msgs.append(msg)
            tl.write('\r\n')
            time.sleep(1)
        msgs=' '.join(msgs)
        print("%s"%msgs)
        tl.close()
        if 'show_msg' in locals().keys() :
            _searchchar(searchchar,show_msg,expect,'show')
        else:
            _searchchar(None,msgs,expect)
        
if __name__ == '__main__' :
    cmmands='conf t;interface ge0/0 ;end; show interface ge0/0'
    a=telnet_test()
    a.telnet_run(host='192.168.15.152',commands=cmmands,expect=1,searchchar='ge0/0')
    #a=telnet_test()
    #cmmands="ip dns static add address=172.16.1.100 name=www.sunyainfo.com;ip dns static add address=172.16.1.100 name=www.qq.com;ip dns static add address=172.16.1.100 name=www.sunyainfo1.com;ip dns static add address=172.16.1.100 name=www.sunyainfo2.com"
    #a.telnet_ros_run(host='192.168.2.165',commands=cmmands,expect=1,searchchar='NETWORK')