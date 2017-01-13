# -*- coding:utf-8 -*-  
import time,sys
from selenium import webdriver
from page_element import page_element
from selenium.common.exceptions import NoSuchElementException,NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC,select
from AutomatedLib.configure import dut_user,dut_passwd,firefoxProfileDir
from AutomatedLib.lib.pub_lib import _working_pc_version,ExpectError

class page_action:
    browser=''
    implicitly_wait=5#设置智能等待时间，隐式等待一个元素被发现，最长时间60s，默认是0
    element=page_element()
    def __init__(self):
        pass
        
    def web_login(self,host,user=dut_user,passwd=dut_passwd,profileDir=firefoxProfileDir):
        print("run keyword:%s "%(sys._getframe().f_code.co_name))
        if 'xp' in _working_pc_version() or '2003' in _working_pc_version() :
            print("Open browser Firefox")
            profile=webdriver.FirefoxProfile(profileDir)
            self.browser=webdriver.Firefox(profile)
        elif 'win7' in _working_pc_version() :
            print("Open brower Chrome")
            self.browser=webdriver.Chrome()
        self.browser.implicitly_wait(self.implicitly_wait)  
        host='http://'+host
        print("browser open url %s"%host)
        self.browser.get(host) 
        self.browser.find_element_by_name("usr").send_keys(user)
        self.browser.find_element_by_name("pwd").send_keys(passwd)
        self.browser.find_element_by_tag_name("button").click()
        print("login %s"%host)
        
    def web_logout(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        self.browser.refresh()#刷新页面
        self.browser.find_element_by_xpath(self.element._get_logout_element()).click()
        self.browser.quit()
        print("close browser~")
    
    def _features_page(self,way):
        '''
        进入到功能页面，格式 分类-模块-功能（-子功能）
        示例：
        self._features_page("策略-防护策略-入侵防护-入侵防护策略")
        self._features_page("策略-防护策略-黑名单")
        '''
        way=way.split('-')
        #self.browser.switch_to.parent_frame() #进入到iframe后回到进入前的界面
        #self.browser.switch_to_default_content() #进入到iframe后回到root界面
        print("into page %s"%str('-'.join(way)))
        self.browser.refresh()#刷新页面
        if len(way) >= 2 :
            self.browser.find_element_by_xpath(self.element._get_classification_element(way[0])).click()
            self.browser.find_element_by_xpath(self.element._get_module_element(way[1])).click()
            if len(way) == 3:
                self.browser.find_element_by_xpath(self.element._get_function_element(way[2])).click()
                if len(way) == 4:
                    self.browser.find_element_by_xpath(self.element._get_function_element(way[3])).click()
        else :
            raise ExpectError("number of args is error ,please check.")
        self.browser.switch_to_frame("Main_con")#进入到iframe Main_con
        
    def _status_check(self,name,status,expect,message=None):
        if str(status) == str(expect) :
            print("status check Success , %s current status : %s,  expect status : %s"%(name,status,expect))
        else :
            if message==None :
                raise ExpectError("status check False , %s current status : %s,  expect status : %s"%(name,status,expect))
            else :
                raise ExpectError("status check False , %s current status : %s,  expect status : %s  message=%s"%(name,status,expect,message))
    
    def _iframe_policy_menu(self,name):
        '''
        策略的菜单：新建、删除、启用、禁用、移动 操作按钮。
        '''
        print("click policy menu %s"%name)
        self.browser.find_element_by_xpath(self.element._get_iframe_menu_element(name)).click()
    
    
    def _iframe_input_box(self,name,value):
        print("input box %s  %s"%(name,value))
        element=self.browser.find_element_by_xpath(self.element._get_iframe_input_box_element(name))
        element.clear()
        element.send_keys("%s"%value)
        #self.browser.find_element_by_xpath(self.element._get_iframe_input_box_element(name)).send_keys("%s"%value)
        
    def _iframe_input_box_expect(self,name,value,expect):
        print("check value of input box.")
        msg=None
        try:
            self.browser.find_element_by_xpath('//*[contains(text(),\'%s\')]'%value)
            status = True
        except NoSuchElementException,message:
            status = False
            msg=message
        self._status_check('input box expect',status,expect,msg)
        
    def _iframe_select(self,name=None,value=None):
        print("drop down %s,value %s"%(name,value))
        xpath_name,xpath_value=self.element._get_iframe_select_element(name,value)
        sele=select.Select(self.browser.find_element_by_xpath(xpath_name))
        sele.select_by_visible_text(value)
    
    def _iframe_select_expect(self,name=None,value=None,expect=None):
        print("check drop down %s,value %s"%(name,value))
        xpath_name,xpath_value=self.element._get_iframe_select_element(name,value)
        sele=select.Select(self.browser.find_element_by_xpath(xpath_name))
        if sele.all_selected_options() == value:
            status = True
        else :
            status = False
        self._status_check('select expect',status,expect)
        
    def _iframe_submit_options(self,option):
        '''
        策略配置页面 确定/提交/取消 按钮操作。
        '''
        print("button click %s"%option)
        self.browser.find_element_by_xpath(self.element._get_iframe_submit_options_element(option)).click()
    
    def _iframe_policy_expect(self,policy,expect):
        '''
        期望出现的策略
        '''
        print("check policy %s, expect is %s"%(policy,expect))
        msg=None
        try:
            self.browser.find_element_by_xpath(self.element._get_iframe_policy_element(policy))
            status = True
        except NoSuchElementException,message:
            status = False
            msg=message
        self._status_check('policy ',status,expect,msg)
    
    def _iframe_conf_checkbox(self,name,expect_status):
        '''
        配置中的复选框
        '''
        print("click checkbox %s, expect status %s"%(name,expect_status))
        checkbox_element=self.browser.find_element_by_xpath(self.element._get_iframe_conf_checkbox_element(name))
        if str(checkbox_element.is_selected()) != expect_status :
            checkbox_element.click()
    
    def _iframe_conf_checkbox_expect(self,name,expect):
        '''
        检查复选框
        '''
        print("check checkbox %s, expect status %s"%(name,expect_status))
        if self.browser.find_element_by_xpath(self.element._get_iframe_conf_checkbox_element(name)).is_selected() :
            status = True
        else :
            status = False
        self._status_check('conf page , check box expect',status,expect)
    
    def _iframe_radio(self,name,expect_status):
        '''
        单选框
        '''
        print("click radio %s, expect status %s"%(name,expect_status))
        radio_element=self.browser.find_element_by_xpath(self.element._get_iframe_radio_element(name))
        if str(radio_element.is_selected()) != expect_status :
            radio_element.click()
            
    def _iframe_radio_expect(self,name,expect):
        print("check radio %s, expect status %s"%(name,expect_status))
        if self.browser.find_element_by_xpath(self.element._get_iframe_conf_checkbox_element(name)).is_selected() :
            status = True
        else :
            status = False
        self._status_check('radio expect',status,expect)
    
    def _iframe_policy_checkbox(self,name):
        '''
        显示配置中，策略前的复选框
        '''
        attempts =0
        success = False
        while attempts < 2 and not success:
            try:
                self.browser.find_element_by_xpath(self.element._get_iframe_policy_checkbox_element(name,attempts)).click()
                success = True
            except NoSuchElementException :
                attempts+=1
                if attempts == 2 :
                    success = False
        if success == True :
            pass
        else :
            raise NoSuchElementException 

    def _iframe_policy_click(self,policy,action):
        '''policy that we will edit，format like  test:any:any:any:any ;the first better is a clicked element,like policy id or name.
        action , link "move" or "delete" that will be clicked.
        | self._iframe_policy_click | ge0/0:any:any:any:permit | 删除 |
        '''
        print("policy click :%s , action:%s"%(policy,action))
        self.browser.find_element_by_xpath(self.element._get_iframe_policy_click_element(policy,action)).click()
    
    def _iframe_config(self,config):
        config=config.split(':')
        if config[0] == 'input' :
            if len(config) == 3 :
                self._iframe_input_box(config[1],config[2])
            else:
                raise ExpectError("number of args is error ,please check.")
        elif config[0] == 'select':
            if len(config) == 2 :
                self._iframe_select(name=None,value=config[1])
            elif len(config) == 3:
                self._iframe_select(name=config[1],value=config[2])
            else:
                raise ExpectError("number of args is error ,please check.")
        elif config[0] == 'checkbox':
            if len(config) == 3 :
                self._iframe_conf_checkbox(config[1],config[2])
            else:
                raise ExpectError("number of args is error ,please check.")
        elif config[0] == 'radio':
            if len(config) == 3 :
                self._iframe_radio(config[1],config[2])
            else:
                raise ExpectError("number of args is error ,please check.")
        elif config[0] == 'submit':
            if len(config) == 2 :
                self._iframe_submit_options(config[1])
            else:
                raise ExpectError("number of args is error ,please check.")
    
    def _iframe_policy_alert(self,option):
        #if EC.alert_is_present :
            #print("Alert exists")
        try:
            alert=self.browser.switch_to_alert()
            print("alert text:%s"%alert.text)
            if option == True :
                alert.accept()
                print("Alert acepted")
            elif option == False :
                alert.dismiss()
                print("Alert dismiss")
            else:
                raise
        except NoAlertPresentException :
            print("No alert exists")
            
    
    def web_policy_new(self,feature_path,configs,confirm,expect=None,SearchPolicy=None):
        '''
        新增策略关键字：
        feature_path:功能路径，例 策略-防护策略-入侵防护 使用短横线（-）连接
        configs:策略配置 例 [input:名称:test][checkbox:启用,True][select:入接口:any][submit:提交],其中，每个选项的配置用中括号括起来；中括号中用冒号分割的值分别对应配置类型、配置字段、配置值。
            配置类型：复选框（checkbox),单选框（radio），输入框（input），下拉框（select），菜单动作（menu），提交（submit）
            配置字段：字段名称
            配置的值：输入（选择）的值
            下拉框前没有名称，可直接输入选项 如 接口管理页面 ip地址类型下拉框可直接写成 select:IPv6
        confirm:提交/取消 策略提交按钮的名称
        expect：True/False/None,期望
        SearchPolicy: test:any:any:any:any:Common    期望添加的策略
        例：
        | web_policy_new | 策略-防护策略-入侵防护 | [input:名称:test][checkbox:启用,True][select:入接口:any][select:出接口:any][select:源地址:any][select:目的地址:any][select:事件集:Common][checkbox:日志] | 提交 | True | test:any:any:any:any:Common |
        '''
        print("run keyword:%s "%(sys._getframe().f_code.co_name))
        self._features_page(feature_path)
        self._iframe_policy_menu("新建")
        for i in ('[',']') :
            configs=configs.replace(i,' ')
        configs=configs.split()
        for config in configs :
            self._iframe_config(config)
        self._iframe_submit_options(confirm)
        if expect != None or expect != 'None' :
            self._iframe_policy_expect(SearchPolicy,expect)
    
    def web_policy_edit(self,feature_path,policy,configs,confirm,expect=None,SearchPolicy=None):
        '''
        编辑策略关键字：
        feature_path:功能路径，例 策略-防护策略-入侵防护 使用短横线（-）连接
        policy 策略，例 web访问策略 1:any:any  第一个字段一定是被click的元素（如果可以被click）。
        configs:策略配置 
            例:[input:名称:test][checkbox:启用][select:入接口:any],
            其中，每个选项的配置用中括号括起来；中括号中用冒号分割的值分别对应配置类型、配置字段、配置值。
            配置类型：复选框（checkbox),单选框（radio），输入框（input），下拉框（select），菜单动作（menu），提交（submit）
            配置字段：字段名称
            配置的值：输入（选择）的值
        confirm:提交/取消 策略提交按钮的名称
        expect：True/False/None,期望
        SearchPolicy: test:any:any:any:any:Common    期望添加的策略
        | web_policy_edit | 策略-防护策略-入侵防护 | test:any:any:any:any:Common | [checkbox:启用,False] | 提交 | True | test:any:any:any:any:Common |
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        self._features_page(feature_path)
        self._iframe_policy_click(policy,'编辑')
        for i in ('[',']') :
            configs=configs.replace(i,' ')
        configs=configs.split()
        for config in configs :
            self._iframe_config(config)
        self._iframe_submit_options(confirm)
        if expect != None or expect != 'None' :
            self._iframe_policy_expect(SearchPolicy,expect)
    
    def web_policy_del(self,feature_path,policys,option=True,expect=None):
        '''
        删除策略关键字
        feature_path:功能路径，例 策略-防护策略-入侵防护 使用短横线（-）连接
        policys:删除的策略，例 test:any:any:any:any:Common ;同时删除多个策略，每条策略用中括号括起来 eg [test:any:any:any:any:Common][test:any:any:any:any:Common]
            例 All:ID:状态:用户:地址 这个关键字会删除所有策略。
        option : True/False/None  确认是否删除策略
        expect:期望结果 True/False/None 
        例：
        删除单条策略
        | web_policy_del | 策略-防护策略-入侵防护 | test:any:any:any:any:Common | True | True |
        （说明：expect=True,期望策略被删除。）
        
        删除多条策略
        | web_policy_del | 策略-防护策略-入侵防护 | [test:any:any:any:any:Common][test1:any:any:any:any:Common][test2:any:any:any:any:Common] | True | True |
        （说明：expect=True,期望策略被删除。）
        
        删除所有策略:适用于策略前面有复选框的删除全部策略动作
        | web_policy_del | 对象-用户-用户 | All:用户名:类型:绑定IP:排除IP:状态:引用:操作 | True | True |
        
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        self._features_page(feature_path)
        if str(option) == str(True) :
            submit='确定'
        else :
            submit='取消'
        if '[' in policys :
            for i in ('[',']'):
                policys=policys.replace(i,' ')
            policys=policys.split(' ')
        if policys.split(':')[0].lower() == 'all':
            policy=[]
            for i in range(len(policys.spolit(':'))-1) :
                policy[i]=policys[i+1]
            policy=':'.join(policy)
            self._iframe_policy_checkbox(policy)
            self._iframe_policy_menu('删除')
            self._iframe_policy_alert(option)
            self._iframe_submit_options(submit)
        else:
            if type(policys) == list :
                for i in range(loops):
                    self._iframe_policy_click(policys[i],'删除')
                    self._iframe_policy_alert(option)
                    self._iframe_submit_options(submit)
            else:
                self._iframe_policy_click(policys,'删除')
                self._iframe_policy_alert(option)
                self._iframe_submit_options(submit)
        if expect != None or expect != 'None' :
            if str(expect) == str(True) :
                expect = False
            else:
                expect = True
            if type(policys) == list :
                for i in range(len(policys)):
                    self._iframe_policy_expect(policys[i],expect)
            else:
                self._iframe_policy_expect(policys,expect)
     
    def web_policy_move():
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        pass
    
    def web_config_page(self,feature_path,configs,expect):
        '''
        
        
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        self._features_page(feature_path)
        for i in ('[',']') :
            configs=configs.replace(i,' ')
        configs=configs.split()
        for config in configs :
            self._iframe_config(config)
        self._iframe_submit_options(confirm)
        
    
if __name__ == '__main__':
    a=page_action()
    a.web_login('172.17.1.12')
    a.web_policy_new("策略-防护策略-入侵防护",'[input:名称:test][checkbox:启用:True][select:入接口:any][select:出接口:any][select:源地址:any][select:目的地址:any][select:事件集:Common][checkbox:日志:True]','提交',True,'test:any:any:any:any:Common')
    a.web_policy_edit("策略-防护策略-入侵防护",'1:test:any:any:any:any:Common','[checkbox:启用:False][checkbox:日志:True]','更新',True,'test:any:any:any:any:Common')
    time.sleep(5)
    a.web_policy_del("策略-防护策略-入侵防护",'test:any:any:any:any:Common',True,True)
    time.sleep(5)
    a.web_logout()