class CurrencyVector:
    def __init__(self, **kwargs):
        self._amounts = dict(kwargs)

    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(f'{CUR} = {amount}' for CUR, amount in self._amounts.items()) + ')'


    def __add__(self, other):
        if not isinstance(other, CurrencyVector):
            return NotImplemented
        result = {}
        for currency in set(self._amounts) | set(other._amounts):
            csum = self._amounts.get(currency, 0) + other._amounts.get(currency, 0)
            if csum:
                result[currency] = csum
        return CurrencyVector(**result)

    def __sub__(self, other):
        if not isinstance(other, CurrencyVector):
            return NotImplemented
        result = {}
        for currency in set(self._amounts) | set(other._amounts):
            csum = self._amounts.get(currency, 0) - other._amounts.get(currency, 0)
            if csum:
                result[currency] = csum
        return CurrencyVector(**result)

    def __eq__(self, other):
        return not(self - other)

    def items(self):
        return self._amounts.items()

    def __bool__(self):
        return any(self._amounts.values())



if __name__ == '__main__':
    a = CurrencyVector(CHF=5)
    b = CurrencyVector(CHF=3, EUR=2)
    print(a+b)
