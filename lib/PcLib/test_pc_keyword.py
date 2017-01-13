# -*- coding:utf-8 -*-  
import unittest
from AutomatedLib.lib.PcLib import pc_keyword


class pctest(unittest.TestCase):
    def setUp(self):
        self.pc=pc_keyword.winpc_keyword()
    def tearDown(self):
        pass
    
    def test_working_pc_version(self):
        self.assertEqual(self.pc._working_pc_version(),2,'not win7')
    
    
    
if __name__ == '__main__':
    unittest.main()