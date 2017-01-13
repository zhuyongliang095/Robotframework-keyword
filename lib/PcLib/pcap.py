# -*- coding:utf-8 -*-  
from scapy.all import *
import threading,sys
from AutomatedLib.lib.pub_lib import _searchchar,_unicode_to_utf,ExpectError,global_encoding
from AutomatedLib.lib.PcLib.pc_keyword import winpc_keyword

class pcap():
    capture_t=''
    cap=''
    def __init__(self):
        pass
    
    def _capture_filter(self,inter='test',filter=None,count=10,timeout=30):
        self.cap=sniff(iface=inter,filter=filter,count=count,timeout=timeout)
        
    def capture_filter(self,inter='test',filter=None,count=10,timeout=10):
        """
        Function: grab pcakets and filter
        eg:
        | Capture Filter | test | udp | count=10 | timeout=30 |
        Caputre pcakets from iface test, filter udp ,expect have packet from 192.168.2.1 to 172.16.0.1 .
        10 pcakets or 30 second to be end.
        
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        id=winpc_keyword()
        ifnet=id.win_show_ip(inter=_unicode_to_utf(inter),searchip='((\d{1,3}\.){3}\d{1,3})/\d{1,2}',ip_type=4,times=15)
        filter=_unicode_to_utf(filter)
        count=int(_unicode_to_utf(count))
        self.timeout=timeout=int(_unicode_to_utf(timeout))
        if filter == 'None' :
            filter = None 
        print("ifnet:%s"%ifnet)
        inter=scapy.all.conf.route.route(str(ifnet))[0]
        print("capture pcap inter=%s, filter=%s,count=%d,timeout=%d"%(inter,filter,count,timeout))
        self.capture_t=threading.Thread(target=self._capture_filter,args=(inter,filter,count,timeout))
        self.capture_t.daemon=False
        self.capture_t.start()
        print("start capture pcakets!")
        
    def capture_show(self,searchc=None,expect=1):
        """
        Function: show capture pcakets
        eg:
        | Capture Show | 192.168.0.100 | 1 |
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        searchc=_unicode_to_utf(searchc)
        expect=int(_unicode_to_utf(expect))
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        print("wait for capture pcakets!")
        time.sleep(int(self.timeout))
        pcap=[]
        if self.capture_t.is_alive() :
            self.capture_t.terminate()
            self.capture_t.join()
        for i in self.cap:
            pcap.append(str(i.show))
        strpcap='\n'.join(pcap)
        print("%s"%strpcap)
        return _searchchar(searchc,strpcap,expect,tpye='pcap')
        
if __name__ == '__main__' :
    a=pcap()
    a.capture_filter(inter='mgt',filter='tcp',count=10,timeout=30)
    time.sleep(20)
    a.show_capture(search='TCP',expect=1)