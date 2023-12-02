from decimal import Decimal

from .models import Entry, Account, Currency

def revolut(data):
    if data['Type'] == 'CARD_PAYMENT':
        bank_acc = {
            'CHF': Account.objects.get(pk='110007')
        }[data['Currency']]
        currency = Currency.objects.get(pk=data['Currency'])
        expense_acc = Account.objects.get(pk='419001')
        expense_amt = -Decimal(data['Amount'])
        fee_amt = Decimal(data['Fee'])
        fee_acc = Account.objects.get(pk='481001')

        if expense_amt < 0:
            return
        if fee_amt < 0:
            return

        entries = [
            Entry(account=bank_acc, currency=currency, etype=Entry.CREDIT, amount=-expense_amt - fee_amt),
            Entry(account=expense_acc, currency=currency, etype=Entry.DEBIT, amount=expense_amt),
        ]
        if fee_amt:
            entries.append(Entry(account=fee_acc, currency=currency, etype=Entry.DEBIT, amount=fee_amt))
        yield 1.0, entries
    elif data['Type'] == 'TOPUP':
        pass