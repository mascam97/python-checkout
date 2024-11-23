import unittest

from entities.amount_base import AmountBase

class AmountBaseTest(unittest.TestCase):
    
    def test_amount_base_inizalitation(self):
        
        amount_base = AmountBase(currency='USD',total=10000);
        
        assert amount_base.currency == 'USD'
        assert amount_base.total == 10000
        
    def test_amount_base_default_values(self):
        amount_base = AmountBase(total=10000);
        
        assert amount_base.currency == 'COP'
        assert amount_base.total == 10000