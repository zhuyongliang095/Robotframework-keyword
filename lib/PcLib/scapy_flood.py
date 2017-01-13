#!/user/bin/python27
# -*- coding: utf-8 -*-  
from scapy.all import *
import sys
from AutomatedLib.lib.pub_lib import _unicode_to_utf

class scapy_flood:

    def __init__(self):
        pass

    def IP_change(self,IP=None,count=None):
        '''IP变化,变化后2位.例
        | IP change | IP | count |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        IP=_unicode_to_utf(IP)
        count=_unicode_to_utf(count)
        count=int(count)
        ip=[]
        ip_3=int(IP.split('.')[-2])
        ip_4=int(IP.split('.')[-1])
        ip_12='%s.%s' % (IP.split('.')[0],IP.split('.')[1])

        for i in range(count):
            ip_4new=ip_4+i
            if 0<ip_4new<=254:
                ip.append(('%s.%s.%s') % (ip_12,ip_3,ip_4new))
            else:
                    ip_3new=ip_3+int(ip_4new/254)
                    ip_4new=ip_4new%254
                    ip.append(('%s.%s.%s') % (ip_12,ip_3new,ip_4new))
        return ip
    def _sendarp(self,ip):
        a=[]
        for i in range(len(ip)):
            a.append(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip[i]))
        sendp(a,count=1)

    def sendarp(self,IP=None,count=None):
        '''发送arp请求报文.例
        | sendarp | IP | count |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        IP=_unicode_to_utf(IP)
        count=_unicode_to_utf(count)
        ip=self.IP_change(IP,count)
        self._sendarp(ip)
        
    def _sendudp(self,dmac,ip,dip,port):
        a=[]
        for i in range(len(ip)):
            isport=random.randint(1,65535)
            a.append(Ether(dst=dmac)/IP(src=ip[i],dst=dip)/UDP(sport=isport,dport=port))
        sendp(a,count=1)
        
    def udpflood(self,dip=None,dmac=None,port=None,count=None,IP=None):
        '''向指定的dip和目的端口发送udp报文，源端口随机变化，参数含义：
        dip：目的ip
        dmac：目的mac
        port：目的端口
        count：变化个数
        IP：起始源ip，根据count数递增
        | udpflood | dip | dmac | port | count | IP |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        dmac=_unicode_to_utf(dmac)
        port=_unicode_to_utf(port)
        count=_unicode_to_utf(count)
        IP=_unicode_to_utf(IP)
        
        ip=self.IP_change(IP,count)
        self._sendudp(dmac,ip,dip,port)
        
    def _sendtcp(self,dmac,ip,dip,port):
        a=[]
        for i in range(len(ip)):
            isport=random.randint(1,65535)
            a.append(Ether(dst=dmac)/IP(src=ip[i],dst=dip)/TCP(sport=isport,dport=port,flags='S'))
        sendp(a,count=1)
        
    def tcpflood(self,dip=None,dmac=None,port=None,count=None,IP=None):
        '''向指定的dip和目的端口发送tcp，syn报文，源端口随机变化，参数含义：
        dip：目的ip
        dmac：目的mac
        port：目的端口
        count：变化个数
        IP：起始源ip，根据count数递增
        | tcpflood | dip | dmac | port | count | IP |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        dmac=_unicode_to_utf(dmac)
        port=_unicode_to_utf(port)
        count=_unicode_to_utf(count)
        IP=_unicode_to_utf(IP)
        
        ip=self.IP_change(IP,count)
        self._sendtcp(dmac,ip,dip,port)
    
    def _sendicmp(self,dmac,ip,dip):
        a=[]
        for i in range(len(ip)):
            a.append(Ether(dst=dmac)/IP(src=ip[i],dst=dip)/ICMP())
        sendp(a,count=1)
        
    def icmpflood(self,dip=None,dmac=None,count=None,IP=None):
        '''向指定的dip发送icmp报文，参数含义：
        dip：目的ip
        dmac：目的mac
        count：变化个数
        IP：起始源ip，根据count数递增
        | icmpflood | dip | dmac | count | IP |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        dmac=_unicode_to_utf(dmac)
        count=_unicode_to_utf(count)
        IP=_unicode_to_utf(IP)
        
        ip=self.IP_change(IP,count)
        self._sendicmp(dmac,ip,dip)
        
    def sendudp6(self,dip=None,port=None,count=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        port=_unicode_to_utf(port)
        count=_unicode_to_utf(count)
        a=[]
        count=int(count)
        for i in range (count):
            isport=random.randint(1,65535)
            a.append(IPv6(dst=dip)/UDP(sport=isport,dport=port))
        send(a)
        
    def sendtcp6(self,dip=None,dmac=None,port=None,sip_start=None,sip_end=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        dmac=_unicode_to_utf(dmac)
        port=_unicode_to_utf(port)
        sip_start=_unicode_to_utf(sip_start)
        sip_end=_unicode_to_utf(sip_end)
        
        isport=random.randint(1,65535)
        a=IPv6(dst=dip)/UDP(sport=isport,dport=port)
        send(a)
        
    def sendicmp6(self,dip=None,dmac=None,sip_start=None,sip_end=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        dip=_unicode_to_utf(dip)
        dmac=_unicode_to_utf(dmac)
        sip_start=_unicode_to_utf(sip_start)
        sip_end=_unicode_to_utf(sip_end)
        
        isport=random.randint(1,65535)
        a=IPv6(dst=dip)/ICMPv6EchoRequest()
        send(a)
        
if __name__=='__main__':

    a=scapy_flood()
    a.sendudp6(dip='2001::2',port=53,count=10)
