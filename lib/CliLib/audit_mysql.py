# -*- coding:utf-8 -*-  
import telnetlib,re,sys,time
from AutomatedLib.lib.pub_lib import _unicode_to_utf,ExpectError,_searchchar
from AutomatedLib.configure import dut_user,dut_passwd

class audit_mysql:
    timeout=5
    def __init__(self):
        pass
    
    def _login_diagnose(self,host,username,passwd):
        msgs=[]
        tl=telnetlib.Telnet(host,23,10)
        msg=tl.read_until("Username:",self.timeout)
        time.sleep(1)
        msgs.append(msg)
        tl.write(username+'\n')
        msg=tl.read_until("Password:",self.timeout)
        msgs.append(msg)
        tl.write(passwd+'\n')
        msg=tl.read_until('>',self.timeout)
        msgs.append(msg)
        tl.write('enable\n')
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        tl.write('diagnose\n')
        msg=tl.read_until('Password:',self.timeout)
        msgs.append(msg)
        tl.write('doitbest\n')
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        return tl,msgs
    
    def _find_current_table(self,tl,table,msgs):
        tl.write("echo \"use syslog; show tables;\" | mysql\n")
        msg=tl.read_until('#',self.timeout)
        pattern=re.compile(r"%s_[0-9]{8}"%table)
        tables_data=[]
        for pat in pattern.finditer(msg):
            tables_data.append(re.split('_',pat.group())[-1])
        for i in range(len(tables_data)-1): 
            if tables_data[i] > tables_data[i+1]:
                tables_data[i],tables_data[i+1]=tables_data[i+1],tables_data[i]
        msgs.append(msg)
        return table+"_"+tables_data[len(tables_data)-1] 
        
    def audit_drop_tables(self,host='',username=dut_user,passwd=dut_passwd):
        '''
        clear mysql syslog tables.
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        username=_unicode_to_utf(username)
        passwd=_unicode_to_utf(passwd)
        tl,msgs=self._login_diagnose(host,username,passwd)
        tl.write("echo \"use syslog; show tables;\" | mysql\n")
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        pattern=re.compile(r"[a-z_]*_[0-9]{8}")
        tables_data=[]
        for pat in pattern.finditer(msg):
            tables_data.append(pat.group())
        for i in tables_data:
            tl.write("echo \"use syslog; drop table "+i+";\" | mysql\n")
            msg=tl.read_until('#',self.timeout)
            msgs.append(msg)
        tl.write("echo \"use syslog; show tables;\" | mysql\n")
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        tl.close()
        msgs=' '.join(msgs)
        print("%s"%msgs)
            
    def audit_mysql_search(self,host='',table='',expect=None,searchchar=None,username=dut_user,passwd=dut_passwd):
        '''
        table=file_transfer,app_others,email,instant_message,online_shopping,search-enine,social_network
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        table=_unicode_to_utf(table)
        expect=_unicode_to_utf(expect)
        searchchar=_unicode_to_utf(searchchar)
        username=_unicode_to_utf(username)
        passwd=_unicode_to_utf(passwd)
        
        tl,msgs=self._login_diagnose(host,username,passwd)
        table_name=self._find_current_table(tl,table,msgs)
        tl.write("echo \"use syslog; select * from "+table_name+"; \" | mysql\n")
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        tl.close()
        msgs=' '.join(msgs)
        print("%s"%msgs)
        _searchchar('ERR',msg,0,'sql')
        _searchchar(searchchar,msg,expect,'sql')

    def audit_mysql_table_clear(self,host='',table='',username=dut_user,passwd=dut_passwd):
        '''
        table=file_transfer,app_others,email,instant_message,online_shopping,search-enine,social_network
        '''
        host=_unicode_to_utf(host)
        table=_unicode_to_utf(table)
        username=_unicode_to_utf(username)
        passwd=_unicode_to_utf(passwd)
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        tl,msgs=self._login_diagnose(host,username,passwd)
        table_name=self._find_current_table(tl,table,msgs)
        tl.write("echo \" use syslog; truncate table "+table_name+";\" | mysql\n")
        msg=tl.read_until('#',self.timeout)
        msgs.append(msg)
        tl.close()
        msgs=' '.join(msgs)
        print("%s"%msgs)
        
if __name__ == '__main__' :
    a=audit_mysql()
    a.audit_mysql_search(host='192.168.2.58',table='file_transfer',expect=1,searchchar='172.16.0.100.*172.16.1.100.*21.*FTP.*anonymous.*test.iso')
    a.audit_mysql_table_clear(host='192.168.2.58',table='file_transfer')
    a.drop_tables(host='192.168.2.58')