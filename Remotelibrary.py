# -*- coding:utf-8 -*-  
import sys
from lib.PcLib.file_test import file_test
from lib.PcLib.email_test import mail_test
from lib.PcLib.http_test import http_keyword
from lib.PcLib.pc_keyword import winpc_keyword
from lib.PcLib.socket_transmission import socket_transmission
#from lib.PcLib.scapy_flood import scapy_flood
#from lib.PcLib.pcap import pcap

from lib.CliLib.telnet_test import telnet_test
from lib.CliLib.clear_all_conf import clear_all_conf
from lib.CliLib.audit_mysql import audit_mysql

from lib.remote_run_key import remote_run_key
from lib.pub_lib import lib_update

from lib.WebLib.page_action import page_action
from lib.APIlib.wafapi import wafapi

class import_remote_key(#mail_test, \
                        #file_test, \
                        http_keyword, \
                        remote_run_key, \
                        #telnet_test, \
                        winpc_keyword, \
                        #clear_all_conf, \
                        #audit_mysql, \
                        #socket_transmission, \
                        #pcap,\
                        lib_update,\
                        #page_action,\
                        wafapi):
    def __init__(slef):
        pass

if __name__ == '__main__': 
    from robotremoteserver import RobotRemoteServer 
    RobotRemoteServer(import_remote_key(), *sys.argv[1:])