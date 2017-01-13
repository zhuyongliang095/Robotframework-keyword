# -*- coding:utf-8 -*-  

from AutomatedLib.lib.pub_lib import _unicode_to_utf,_searchchar,ExpectError,global_encoding
import subprocess,re,encodings,sys,re,platform,encodings,chardet,time

class winpc_keyword(object):
    def __init__(self):
        pass

    def _working_pc_version(self):
        if re.search('2003',platform.release()) or re.search('xp',platform.release()) :
            return 1
        elif re.search('7',platform.release()) :
            return 2
        else :
            raise ExpectError("no support OS")
        
    def _get_inter_id(self,inter_name='test'):
        msgs=[]
        if re.search('2003',platform.release()) :
            cmd='netsh interface ip show interface '+str(inter_name)
        else:
            cmd='netsh interface ipv4 show interface '
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        if re.search('2003',platform.release()) :
            return msgs[0].split('------------------------------------------------------')[1].split('\n')[1].split(':')[1]
        else:
            msgs_tem=[]
            for i in range(len(msgs)):
                msgs_tem.extend(msgs[i].split('\n'))
            for line in msgs_tem:
                if inter_name in line:
                    return line.split()[0]
        
    def win_show_ip(self,inter='test',searchip=None,ip_type=4,times=15):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        inter=_unicode_to_utf(inter)
        searchip=_unicode_to_utf(searchip)
        ip_type=_unicode_to_utf(str(ip_type))
        times=_unicode_to_utf(times)
        if int(ip_type) == 4:
            ip_type=4
        elif int(ip_type) == 6 :
            ip_type=6
        else:
            raise ExpectError("ip type error")
        if int(ip_type) == 4:
            if self._working_pc_version() == 1:
                cmd='netsh interface ip show config "'+inter+'"'
            elif self._working_pc_version() == 2:
                cmd='netsh interface ipv4 show config "'+inter+'"'
        else:
            cmd='ipconfig'
        tm=0
        #cmd='ipconfig'
        for i in range(int(times)):
            try :
                print("%s"%cmd)
                p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
                p.wait()
                msgs.append(p.stdout.read())
                msgs.append(p.stderr.read())
                p.terminate()
                msg='\n'.join(msgs)
                print("%s"%unicode(msg,global_encoding))
                return _searchchar(searchip,msg,expect=1,tpye='pc')
            except :
                tm+=1
                time.sleep(1)
                if tm == int(times):
                    raise ExpectError("search ip %s error"%searchip)
                else:
                    print("search times %d, search error"%tm)

    def win_ip_add(self,inter='test',ip=None,netmask=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        ip=_unicode_to_utf(ip)
        netmask=_unicode_to_utf(netmask)
        msgs=[]
        if self._working_pc_version() == 1:
            cmd='netsh interface ip add address "'+inter+'" '+ip+' '+netmask
        elif self._working_pc_version() == 2:
            cmd='netsh interface ipv4 add address "'+inter+'" '+ip+' '+netmask
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=ip)
        
    def win_gw_add(self,inter='test',gw=None,ip_type=4,metric=1):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        gw=_unicode_to_utf(gw)
        ip_type=_unicode_to_utf(str(ip_type))
        metric=_unicode_to_utf(metric)
        msgs=[]
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if int(ip_type) == 4:
            if int(self._working_pc_version()) == 1:
                #cmd='route add 0.0.0.0 mask 0.0.0.0 '+str(gw)
                cmd='netsh interface ip add address "'+str(inter)+'" gateway='+str(gw)+' gwmetric='+str(metric)
            else:
                cmd='route add 0.0.0.0/0 '+str(gw)+ ' metric '+str(metric)+' if ' + self._get_inter_id(inter)
        else:
            cmd='route -6 add ::/0 '+str(gw)
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=gw,ip_type=ip_type)
        
    def win_gw_del(self,inter='test',gw=None,ip_type=4):
        """
        inter : the name of interface in PC
        gw : gateway
        ip_type : type of ip  is 4(ipv4) or 6(ipv6)
        eg:
        | win_gw_del | inter | gw | ip_type |
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        gw=_unicode_to_utf(gw)
        ip_type=_unicode_to_utf(str(ip_type))
        msgs=[]
        if int(ip_type) == 4:
            ip_type=4
        elif int(ip_type) == 6 :
            ip_type=6
        else:
            raise ExpectError("ip type error")
        if ip_type == 4:
            cmd='route delete 0.0.0.0/0'
        else :
            cmd='route -6 delete ::/0'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=None,ip_type=ip_type)
        
    def win_ip_del(self,inter='test',ip=None,ip_type=4):
        """
        del ip from interface, ip_type is 4(ipv4) or 6(ipv6).
        eg:
        | Win Ip Del | inter | ip | ip_type |
        """
        inter=_unicode_to_utf(inter)
        ip=_unicode_to_utf(ip)
        ip_type=_unicode_to_utf(str(ip_type))
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        if int(ip_type) == 4:
            ip_type=4
        elif int(ip_type) == 6 :
            ip_type=6
        else:
            raise ExpectError("ip type error")
        if int(ip_type) == 4:
            if self._working_pc_version() == 1:
                cmd='netsh interface ip delete address "'+str(inter)+'" addr='+ip+' gateway=all'
            elif self._working_pc_version() == 2:
                cmd='netsh interface ipv4 delete address "'+str(inter)+'" addr='+ip+' gateway=all'
        else:
            directly_route=ip.split('::')[0]+'::/64'
            ip=ip.split('/')[0]
            cmd='netsh interface ipv6 delete route '+directly_route+' "'+inter +'"  && netsh interface ipv6 delete address "'+str(inter)+'" '+ip
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=None,ip_type=ip_type)

    def win_set_dhcp_ip(self,inter='test',searchip=None,ip_type=4,times=30):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        searchip=_unicode_to_utf(searchip)
        ip_type=_unicode_to_utf(str(ip_type))
        times=_unicode_to_utf(times)
        msgs=[]
        if self._working_pc_version()==1 :
            cmd='netsh interface ip set address name="'+inter+'" source=dhcp'
        elif self._working_pc_version()== 2 :
            cmd='netsh interface ipv4 set address name="'+str(inter)+'" source=dhcp '
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter,searchip,ip_type,times)
    
    def win_dhcp_renew(self,inter='test',searchip=None,ip_type=4,times=30):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        searchip=_unicode_to_utf(searchip)
        ip_type=_unicode_to_utf(str(ip_type))
        times=_unicode_to_utf(times)
        msgs=[]
        cmd='ipconfig /renew'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter,searchip,ip_type,times)
    
    def win_dhcp_release(self):
        ''' dhcp release        
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='ipconfig /release'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip()
        
    def win_set_static_ip(self,inter='test',ip=None,netmask='255.255.255.0',ip_type=4):
        '''if ip_type = 4 ,netmask = 255.255.255.0 like.
        if ip_type = 6 ,netmask = 2000:1::/64 like this.
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        ip=_unicode_to_utf(ip)
        netmask=_unicode_to_utf(netmask)
        ip_type=_unicode_to_utf(str(ip_type))
        msgs=[]
        if str(ip_type) == '4':
            ip_type=4
        elif str(ip_type) == '6' :
            ip_type=6
        else:
            raise ExpectError("ip type error")
        if int(ip_type) == 4:
            if self._working_pc_version()==1 :
                cmd='netsh interface ip set address name="'+inter+'" static '+ip+' '+netmask
            elif self._working_pc_version()== 2 :
                cmd='netsh interface ipv4 set address name="'+inter+'" static '+ip+' '+netmask
        else:
            cmd='netsh interface ipv6 set address "'+inter+'" '+ip+' store=active && netsh interface ipv6 add route '+netmask+' "'+inter+'"'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=ip,ip_type=ip_type)
    
    def win_set_dhcp_dns(self,inter='test',search_dns=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        search_dns=_unicode_to_utf(search_dns)
        msgs=[]
        if self._working_pc_version()==1 :
            cmd='netsh interface ip set dns  name="'+inter+'" source=dhcp'
        elif self._working_pc_version()== 2 :
            cmd='netsh interface ipv4 set dnsservers name="'+inter+'" source=dhcp'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=search_dns)
    
    def win_set_static_dns(self,inter='test',dns_ip=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        dns_ip=_unicode_to_utf(dns_ip)
        msgs=[]
        if self._working_pc_version()==1 :
            cmd='netsh interface ip set dns  name="'+inter+'" source=static '+dns_ip
        elif self._working_pc_version()== 2 :
            cmd='netsh interface ipv4 set dnsservers name="'+inter+'" static '+dns_ip
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=dns_ip)

    def win_del_static_dns(self,inter='test',dns_ip='all'):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        dns_ip=_unicode_to_utf(dns_ip)
        msgs=[]
        if self._working_pc_version()==1 :
            cmd='netsh interface ip delete dns "'+inter+'" '+dns_ip
        elif self._working_pc_version()== 2 :
            cmd='netsh interface ipv4 delete dnsservers "'+inter+'" '+dns_ip
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test')
        
    def win_clean_arp(self,inter='test',ip_type=4):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        ip_type=int(_unicode_to_utf(ip_type))
        msgs=[]
        if ip_type == 4 :
            if self._working_pc_version()==1:
                cmd='netsh interface ip delete arpcache name="'+inter+'"'
            elif  self._working_pc_version()==2:
                cmd='netsh interface ipv4 delete arpcache "'+inter+'"'
        elif ip_type == 6 :
            cmd='netsh interface ipv6 delete neighbors "'+inter+'"'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))

    def win_clean_dns_cache(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='ipconfig /flushdns'
        print("%s"%cmd)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))

    def win_ping(self,inter='test',host=None,num=2,times=2,expect=1):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        inter=_unicode_to_utf(inter)
        host=_unicode_to_utf(host)
        num=_unicode_to_utf(num)
        times=_unicode_to_utf(times)
        expect=_unicode_to_utf(expect)
        msgs=[]
        stat=0
        for i in range(int(times)) :
            tmp_msgs=[]
            cmd='ping '+str(host)+' -n '+str(num)
            print("%s"%cmd)
            p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            p.wait()
            tmp_msgs.append(p.stdout.read())
            tmp_msgs.append(p.stderr.read())
            p.terminate()
            msgs.extend(tmp_msgs)
            reobj=re.compile('\(0% loss\)|\(0% 丢失\)')
            tmp_msgs=' '.join(tmp_msgs)
            tmp_msgs=unicode(tmp_msgs,chardet.detect(tmp_msgs)['encoding']).encode('utf-8')
            if reobj.search(tmp_msgs) :
                stat = 1
                break
        print("%s"%unicode('\n'.join(msgs),chardet.detect('\n'.join(msgs))['encoding']))
        if expect != 'None' and expect != None :
            if int(stat) == int(expect) :
                print("Expect is %s, actually %s"%('success' if int(expect) == 1 else 'fail','success' if int(expect) == 1 else 'fail'))
            else:
                raise ExpectError(message="Expect is %s, actually %s"%("Success" if int(expect) == 1 else "failed","success" if int(stat) == 1 else "failed"))

if __name__ == '__main__':
    test=winpc_keyword()
    #test.win_show_ip('test')
    #test.win_set_static_ip('test','40.40.40.1','255.255.255.0')
    #test.win_set_static_ip('test','3000::100','255.255.255.0','6')
    #test.win_ip_add('test','30.30.30.1','255.255.255.0')
    test.win_gw_add('test','172.16.0.1')
    #test.win_ip_del('test','30.30.30.1')
    #test.win_ip_del('test','40.40.40.1')
    #test.win_set_dhcp_ip('test')
    #test.win_dhcp_release()
    #test.win_dhcp_renew()
    #test.win_set_dhcp_dns('test')
    #test.win_set_static_ip('test','40.40.40.1','255.255.255.0')
    #test.win_set_static_dns('test','50.50.50.50')
    #test.win_clean_arp()
    #test.win_ping(inter='test',host='172.16.0.2')
    