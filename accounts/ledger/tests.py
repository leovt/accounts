from django.test import TestCase

from .currencies import CurrencyVector
class CurrenciesTest(TestCase):
    def test_add_same_currency(self):
        a = CurrencyVector(CHF = 12)
        b = CurrencyVector(CHF = 8)
        self.assertEquals(a + b, CurrencyVector(CHF = 20))

    def test_add_different_currencies(self):
        a = CurrencyVector(EUR = 4)
        b = CurrencyVector(CHF = 8)
        self.assertEquals(a + b, CurrencyVector(CHF = 8, EUR = 4))

    def test_add_overlapping_currencies(self):
        a = CurrencyVector(EUR = 4, GBP=100)
        b = CurrencyVector(CHF = 8, GBP=22)
        self.assertEquals(a + b, CurrencyVector(GBP = 122, CHF = 8, EUR = 4))

    def test_sub_same_currency(self):
        a = CurrencyVector(CHF = 12)
        b = CurrencyVector(CHF = 8)
        self.assertEquals(a - b, CurrencyVector(CHF = 4))

    def test_sub_different_currencies(self):
        a = CurrencyVector(EUR = 4)
        b = CurrencyVector(CHF = 8)
        self.assertEquals(a - b, CurrencyVector(CHF = -8, EUR = 4))

    def test_sub_overlapping_currencies(self):
        a = CurrencyVector(EUR = 4, GBP=100)
        b = CurrencyVector(CHF = 8, GBP=22)
        self.assertEquals(a - b, CurrencyVector(GBP = 78, CHF = -8, EUR = 4))

    def test_zero(self):
        zero_CHF = CurrencyVector(CHF = 0)
        zero_EUR = CurrencyVector(EUR = 0)
        self.assertEquals(zero_EUR, zero_CHF)
