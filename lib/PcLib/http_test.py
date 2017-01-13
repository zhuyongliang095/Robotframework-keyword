# -*- coding:utf-8 -*-  

import BaseHTTPServer,httplib,urllib,re,sys,encodings
import urlparse,multiprocessing
from AutomatedLib.lib.pub_lib import _searchchar,_unicode_to_utf,ExpectError,global_encoding
class _WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """
        """
        self.protocol_version='HTTP/1.1'
        msgs='测试！！！！！！！！\n \
        test\n\
        邪教\n\
        さしす\n\
        '
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                '<html>',
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                'message=%s' % msgs,#.decode('utf-8').encode('gbk'),
                '',
                'HEADERS RECEIVED:',
                ]
        self.send_response(200)
        #print("headers connection:%s"%self.headers['connection'])
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('</html>')
        message = '\r\n'.join(message_parts)
        self.send_header('Content-Length',str(len(message)))
        self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(message)

    def do_PSOT(self):
        """
        """
        self.protocol_version='HTTP/1.1'
        msgs='测试！！！！！！！！\n\
        '
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                '<html>',
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                'message=%s' % msgs,#.decode('utf-8').encode('gbk'),
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('</html>')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Length',str(len(message)))
        self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(message)

class http_keyword(object):
    """docstring for http_keyword"""
    serProcess=[]

    def _http_serv_simple(self,ip='0.0.0.0',port=80):
        port=int(port)
        server = BaseHTTPServer.HTTPServer((ip,port), _WebRequestHandler)
        server.serve_forever()

    def http_serv(self,ip='0.0.0.0',port=80):
        '''
            http_cli action get: "测试！！！！！！！！"、"test"、"邪教"、"さしす"
            http_cli action post: "测试！！！！！！！！"
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        ip=_unicode_to_utf(ip)
        port=_unicode_to_utf(port)
        process=multiprocessing.Process(target=self._http_serv_simple,args=(ip,port,))
        process.daemon=True
        process.start()
        self.serProcess.append(process)
        print("http server %s:%s is starting~"%(ip,str(port)))

    def stop_http_serv(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        for i in range(len(self.serProcess))[::-1]:
            self.serProcess[i].terminate()
            self.serProcess[i].join()
            del self.serProcess[i]
            print("http server is killed~")

    def http_cli(self,host='',port=None,url='/',act='GET',expect=1,searchc=None):
        '''
        '''
        host=_unicode_to_utf(host)
        port=_unicode_to_utf(port)
        if (not port) or port == "None" or port.isspace():
            port=None
        url=_unicode_to_utf(url)
        act=_unicode_to_utf(act)
        expect=_unicode_to_utf(expect)
        searchc=_unicode_to_utf(searchc)
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        sendheader={"Accept-Encoding":"gzip, deflate, sdch",\
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",\
                    #"Content-Length":"100",\
                    "Connection":"keep-alive",\
                    "Accept-Language":"zh-CN,zh;q=0.8",\
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        try:
            conn=httplib.HTTPConnection(host=host,port=port)#,timeout=10)
            conn.request(act,url,'',sendheader)
            msgs=conn.getresponse()
            body=msgs.read()
            conn.close()
        except:
            if expect == 0 or expect == '0':
                if searchc ==None or str(searchc) == 'None' or searchc == '':
                    print("expect get url from host:%s fail, actually fail"%host)
                else :
                    raise ExpectError("expect get url from host:%s ,connect fail"%host)
            else :
                raise ExpectError("get url from host:%s error!"%host)
        else:
            if searchc ==None or str(searchc) == 'None' or searchc == '' :
                if expect == 0 :
                    raise ExpectError("expect get url from host:%s fail, actually success"%host)
                else :
                    print("body:\n%s"%unicode(body,'utf8'))
                    print("expect get url from host:%s success, actually sucess"%host)
            else :
                print("body:\n%s"%body)
                _searchchar(searchc,body,expect,'http')


if __name__ == '__main__':
    test=http_keyword()
    test.http_serv()
    test.http_cli(host='127.0.0.1',port=80,url='/',act='GET',expect=1)
    test.stop_http_serv()

