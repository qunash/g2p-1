from unittest import main, TestCase
import os
from g2p.cors import Correspondence
import unicodedata as ud

class CorrespondenceTest(TestCase):
    ''' Basic Correspondence Test
    '''

    def setUp(self):
        # self.test_cor = Correspondence([{'from': 'a', "to": 'b'}])
        # self.test_cor_rev = Correspondence([{"from": 'a', "to": 'b'}], True)
        # self.test_cor_moh = Correspondence(language={"lang": "moh", "table": "orth"})
        self.test_cor_norm = Correspondence([{'from': '\u0061\u0301', 'to': '\u0061\u0301'}])
    
    def test_normalization(self):
        self.assertEqual(ud.normalize('NFC', '\u0061\u0301'), self.test_cor_norm.cor_list[0]['from'])
        self.assertEqual(self.test_cor_norm.cor_list[0]['from'], '\u00e1')
        self.assertNotEqual(self.test_cor_norm.cor_list[0]['from'], '\u0061\u0301')