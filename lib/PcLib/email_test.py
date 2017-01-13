# -*- coding:utf-8 -*-  

import smtplib,os,poplib,sys,string,encodings,imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from AutomatedLib.lib.pub_lib import _unicode_to_utf

class mail_test(object):
    def __init__(self):
        pass

    def stmp_send_text(self,mailto_list='test2@autotest.com',sub='autotest',content='',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        '''mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)
        print("connect to mail server")
        #BuiltIn._Misc.log(message="connect to mail server",level='INFO')
        #me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        me=mail_user+"@"+mail_postfix
        msg=MIMEText(content,'plain',_charset=charset)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = to_list = ';'.join(mailto_list)
        print("send mail !")
        print("stmp send text mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP()
        server.connect(host=mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
            return True
        except:
            print("send mail failed")
            return False
        server.quit()


    def stmp_send_html(self,mailto_list=('test2@autotest.com'),sub='autotest',content='<a href=\'http://192.168.2.105/\'>abc</a>',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        ''' you can send a mail ,than content is a html.
        mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)    

        me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg=MIMEText(content,'html',_charset=charset)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = to_list = ';'.join(mailto_list) 

        print("stmp send html mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
        except:
            print("send mail failed")
        server.quit()   
    
    

    def stmp_send_attachment(self,mailto_list=['test2@autotest.com'],sub='autotest',content='autotest',att_file='e:\/mail\/abc.txt',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        '''mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        att_file : attachment path;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        att_file=_unicode_to_utf(att_file)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)    

        msg=MIMEMultipart()
        att=MIMEText(open(att_file,'rb').read(),'base64',charset)
        att["Content-Type"] = 'application/octet-stream'
        filepath,filename=os.path.split(att_file)
        att["Content-Disposition"] = 'attachment; filename="'+filename+'"'
        msg.attach(att) 

        msgtxt=MIMEText(content,'plain',_charset=charset)
        msg.attach(msgtxt)  

        me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = to_list= ';'.join(mailto_list)
        print("stmp send attachment and text mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
        except:
            print("send mail failed")
        server.quit()   
    

    #---------------------------------------------  

    def stmps_send_text(self,mailto_list=['test2@autotest.com'],sub='autotest',content='',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        '''mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)    
        me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg=MIMEText(content,'plain',_charset=charset)
        msg['Subject'] = sub
        msg['From'] = me
        mailto_list_utf=unicode(mailto_list)
        mailto_list_utf=mailto_list_utf.encode('utf-8')
        mailto_list=mailto_list_utf.split(',')
        msg['To'] = to_list = ';'.join(mailto_list)
        print("stmps send text send text mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP_SSL()
        server.connect(host=mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
        except:
            print("send mail failed")
        server.quit()   
    

    def stmps_send_html(self,mailto_list=['test2@autotest.com'],sub='autotest',content='<a href=\'http://192.168.2.105/\'>abc</a>',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        ''' you can send a mail ,than content is a html.
        mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)    

        me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg=MIMEText(content,'html',_charset=charset)
        msg['Subject'] = sub
        msg['From'] = me
        mailto_list_utf=unicode(mailto_list)
        mailto_list_utf=mailto_list_utf.encode('utf-8')
        mailto_list=mailto_list_utf.split(',')
        msg['To'] = to_list = ';'.join(mailto_list)
        print("stmps send html mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP_SSL()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
        except:
            print("send mail failed")
        server.quit()   
    
    
    

    def stmps_send_attachment(self,mailto_list=['test2@autotest.com'],sub='autotest',content='autotest',att_file='e:\/mail\/abc.txt',mail_host='192.168.2.114',mail_user='test1',mail_pass='123456',mail_postfix='autotest.com',charset='utf-8'):
        '''mailto_list : send mail to user,value is a list(mor user is test1@autotest.com,test2@autotest.com .) ;
        att_file : attachment path;
        charset : code tpye: utf-8,gb2312,and so on;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        mailto_list=_unicode_to_utf(mailto_list).split(',')
        #mailto_list=mailto_list.split(',')
        sub=_unicode_to_utf(sub)
        content=_unicode_to_utf(content)
        att_file=_unicode_to_utf(att_file)
        mail_host=_unicode_to_utf(mail_host)
        mail_user=_unicode_to_utf(mail_user)
        mail_pass=_unicode_to_utf(mail_pass)
        mail_postfix=_unicode_to_utf(mail_postfix)
        charset=_unicode_to_utf(charset)    

        msg=MIMEMultipart()
        att=MIMEText(open(att_file,'rb').read(),'base64',charset)
        att["Content-Type"] = 'application/octet-stream'
        filepath,filename=os.path.split(att_file)
        att["Content-Disposition"] = 'attachment; filename="'+filename+'"'
        msg.attach(att) 

        msgtxt=MIMEText(content,_charset=charset)
        msg.attach(msgtxt)  

        me="hello"+"<"+mail_user+"@"+mail_postfix+">"
        msg['Subject'] = sub
        msg['From'] = me
        mailto_list_utf=unicode(mailto_list)
        mailto_list_utf=mailto_list_utf.encode('utf-8')
        mailto_list=mailto_list_utf.split(',')
        msg['To'] = to_list = ';'.join(mailto_list) 

        print("stmps send attachment and text mail: %s,%s"%(mail_user,mail_pass))
        server=smtplib.SMTP_SSL()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        try:
            server.sendmail(me, to_list, msg.as_string())
            print("send mail successed")
        except:
            print("send mail failed")
        server.quit()   
    
    
    

    def pop3_resv(self,host='192.168.2.114',user='test2',passwd='123456',delete=1):
        '''host: mail Ser IP; user: user; passwd: password;delete : is delete, 1 delete/0 not delete;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        user=_unicode_to_utf(user)
        passwd=_unicode_to_utf(passwd)
        delete=_unicode_to_utf(delete)
        pp=poplib.POP3(host)
        pp.user(user)
        pp.pass_(passwd)
        ret=pp.stat()
        for i in range(1,ret[0]+1):
            down=pp.retr(i)
        print("user: %s  ,resv message~ "%user)
        if int(delete) == 1:
            for i in range(1,ret[0]+1):
                pp.dele(i)
            print("delete message!")
        pp.quit()   
    

    def pop3s_resv(self,host='192.168.2.114',user='test2',passwd='123456',delete=1):
        '''host: mail Ser IP; user: user; passwd: password;delete : is delete, 1 delete/0 not delete;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        user=_unicode_to_utf(user)
        passwd=_unicode_to_utf(passwd)
        delete=_unicode_to_utf(delete)  

        pp=poplib.POP3_SSL(host)
        pp.user(user)
        pp.pass_(passwd)
        ret=pp.stat()
        for i in range(1,ret[0]+1):
            down=pp.retr(i)
        if int(delete) == 1:
            for i in range(1,ret[0]+1):
                pp.dele(i)
        pp.quit()   
    

    def imap4_resv(self,host='192.168.2.114',user='test2',passwd='123456',delete=1):
        '''host: mail Ser IP; user: user; passwd: password;delete : is delete, 1 delete/0 not delete;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        user=_unicode_to_utf(user)
        passwd=_unicode_to_utf(passwd)
        delete=_unicode_to_utf(delete)  

        m=imaplib.IMAP4(host)
        m.login(user,passwd)
        m.select()
        tpy,data=m.search(None,'ALL')
        for num in data[0].split():
            tpy,message=m.fetch(num,'(RFC822)')
        if int(delete) == 1:
            for num in data[0].split():
                m.store(num,'+FLAGS','\\Deleted')
            m.expunge()
        m.close()
        m.logout()  
    

    def imap4s_resv(self,host='192.168.2.114',user='test2',passwd='123456',delete=1):
        '''host: mail Ser IP; user: user; passwd: password;delete : is delete, 1 delete/0 not delete;'''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        user=_unicode_to_utf(user)
        passwd=_unicode_to_utf(passwd)
        delete=_unicode_to_utf(delete)  

        m=imaplib.IMAP4_SSL(host)
        m.login(user,passwd)
        m.select()
        tpy,data=m.search(None,'ALL')
        for num in data[0].split():
            tpy,message=m.fetch(num,'(RFC822)')
        if int(delete) == 1:
            for num in data[0].split():
                m.store(num,'+FLAGS','\\Deleted')
            m.expunge()
        m.close()
        m.logout()