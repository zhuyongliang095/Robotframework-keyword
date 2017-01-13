# -*- coding:utf-8 -*-  

from AutomatedLib.lib.pub_lib import _unicode_to_utf,_searchchar,ExpectError
from AutomatedLib.configure import dut_user,dut_passwd
import telnetlib,re,time

class clear_all_conf(object):
    def __init__(self):
        pass
    def _login(self,ip,port,username,passwd):
        tl=telnetlib.Telnet(ip,port,10)
        tl.write(username+'\n')
        time.sleep(1)
        tl.write(passwd+'\n')
        tl.write('enable\n')
        tl.write('end\n')
        return tl
    
    def clear_all_conf(self,control_ip,control_port,dut_mgt_ip,user=dut_user,passwd=dut_passwd,t=190):
        msgs=[]
        cmds=['enable']
        cmds.append('end')
        cmds.append('erase startup-config ')
        cmds.append('reboot')
        tl=self._login(control_ip,int(control_port),user,passwd)
        for cmd in cmds:
            if cmd == 'reboot':
                tl.write('%s\n' % cmd)
                msg=tl.read_until('y/n')
                tl.write('y\n')
                break
            else:
                tl.write('%s\n' % cmd)
                msg=tl.read_until('#')
                msgs.append(msg)
        tl.close()
        time.sleep(t)
        tl=self._login(control_ip,int(control_port),user,passwd)
        cmds=[]
        cmds.append('conf t')
        cmds.append('interface mgt')
        cmds.append('no ip address 192.168.1.200/24')
        cmds.append('ip address '+dut_mgt_ip+'/16')
        cmds.append('allow all')
        cmds.append('end')
        cmds.append('write memory')
        for cmd in cmds:
            tl.write('%s\n' % cmd)
            msg=tl.read_until('#')
            msgs.append(msg)
        print("%s"%' '.join(msgs))
        tl.close()
        
if __name__ == '__main__' :
    test=clear_all_conf()
    test.clear_all_conf('192.168.2.200','10002','192.168.2.58')