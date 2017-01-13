# -*- coding:utf-8 -*-  
#from AutomatedLib.lib.pub_lib import ExpectError
class page_element:
    def __init__(self):
        pass
    
    def _name_not_none(self,name):
        pass
    
    def _get_logout_element(self):
        xpath='//*[@title=\'退出登录\']'
        #print("%s xpth = %s"%("退出登录",xpath))
        return xpath
    
    
    def _get_classification_element(self,name):
        self._name_not_none(name)
        #xpath='//*[@id=\'headnavli\']//li[contains(text(),\'%s\')]'%str(name)
        xpath='//*[@id=\'headnavli\']//li[text()=\'%s\']'%str(name)
        #print("%s xpth = %s"%(name,xpath))
        return xpath

    def _get_module_element(self,name):
        self._name_not_none(name)
        xpath='//*[@id=\'page_all_conetent\']//span[contains(text(),\'%s\')]'%str(name)
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath

    def _get_function_element(self,name):
        self._name_not_none(name)
        xpath='//*[@id=\'page_all_conetent\']//li[contains(text(),\'%s\')]'%str(name)
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_menu_element(self,name):
    #新建
        self._name_not_none(name)
        #xpath='//*[@id=\'\']/span/span[contains(text(),\'%s\')]'%str(name)
        xpath='//span/span[contains(text(),\'%s\')]'%str(name)
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_select_element(self,name=None,value=None):
    #下拉框
        self._name_not_none(name)
        self._name_not_none(value)
        if name == None :
            xpath_name='//option[text()=\'%s\']/parent::*'%value
            xpath_value='//option[text()=\'%s\']'%value
        else:
            xpath_name='//*[text()=\'%s\']/following-sibling::*/select'%name
            xpath_value='//option[text()=\'%s\']'%value
        #print("%s xpth = %s ; %s xpath = %s"%(str(name),xpath_name,str(value),xpath_value))
        return xpath_name,xpath_value
    
    def _get_iframe_input_box_element(self,name):
    #输入框
        self._name_not_none(name)
        xpath='//*[text()=\'%s\']/following-sibling::td//input'%name
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_submit_options_element(self,name):
    #提交
        self._name_not_none(name)
        xpath='//input[contains(@value,\'%s\')] | //button[contains(text(),\'%s\')]'%(name,name)
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_policy_element(self,name):
    #策略，定位策略元素
        self._name_not_none(name)
        names=name.split(':')
       # xpath='//*[contains(text(),\'%s\']'%names[0]
        for i in range(len(names)):
            if i == 0 :
                xpath='//*[@field]//*[contains(text(),\'%s\')]'%names[0]
            elif i == 1:
                #xpath+='/parent::*/following-sibling::*[@field]//*[contains(text(),\'%s\')]'%names[i]
                xpath+='/ancestor::*/following-sibling::*[@field]//*[contains(text(),\'%s\')]'%names[i]
            else :
                xpath+='/parent::*/following-sibling::*[@field]//*[contains(text(),\'%s\')]'%names[i]
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_conf_checkbox_element(self,name):
    #配置复选框
        self._name_not_none(name)
        xpath='//*[contains(text(),\'%s\')]/following-sibling::*//*[@type=\'checkbox\'] | //*[text()=\'%s\']/*[@type=\'checkbox\']'%(name,name)
        #print("%s config checkbox xpth = %s"%(str(name),xpath))
        return xpath
    
    def _get_iframe_policy_checkbox_element(self,policy,times):
    #策略前复选框
        self._name_not_none(policy)
        xpath=self._get_iframe_policy_element(policy)
        parent=''
        for i in range(1+times):
            parent+='/parent::*'
        xpath=xpath+parent+'/preceding-sibling::*[@field]//input[@type=\'checkbox\']'
        xpath=xpath
        #print("%s policy checkbox xpth = %s"%(str(policy),xpath))
        return xpath
    
    def _get_iframe_radio_element(self,name):
    #单选框
        self._name_not_none(name)
        xpath='//label[text()=\'%s\']/preceding-sibling::*[@type=\'radio\']'%name
        #print("%s xpth = %s"%(str(name),xpath))
        return xpath
        
    
    
    def _get_iframe_policy_click_element(self,policy,action=None):
    #编辑策略
        self._name_not_none(policy) 
        self._name_not_none(action)
        xpath=self._get_iframe_policy_element(policy)#定位到策略最后一个元素
        xpath1=xpath+'/parent::*/preceding-sibling::*[@field]//*[contains(text(),\'%s\') and @href ]'%policy.split(':')[0]
        if action != None:
            xpath2=xpath+'/parent::*/following-sibling::*[@field]//*[@href]/*[@title=\'%s\']'%action
            xpath=xpath1 + ' | ' +xpath2
        #print("%s xpth = %s"%(str(policy if action == None else policy+':'+action),xpath))
        return xpath
    
    
if __name__ == '__main__':
    a=page_element()
    a._get_iframe_policy_checkbox_element('1:any:any',0)
    pass