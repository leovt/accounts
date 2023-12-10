from decimal import Decimal

from .models import Entry, Account, Currency, Transaction, Period

def revolut(data):
    period = Period.objects.get(start__lte=data['Started Date'][:10], end__gte=data['Started Date'][:10])
    transaction = Transaction(description = f"{data['Description']} (Revolut) {data['Started Date']}",
                              period = period,
                            date = data['Started Date'],
    )

    transaction.save()

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
            return transaction
        if fee_amt < 0:
            return transaction


        Entry(account=bank_acc, currency=currency, etype=Entry.CREDIT, amount=-expense_amt - fee_amt, transaction=transaction).save()
        Entry(account=expense_acc, currency=currency, etype=Entry.DEBIT, amount=expense_amt, transaction=transaction).save()

        if fee_amt:
            Entry(account=fee_acc, currency=currency, etype=Entry.DEBIT, amount=fee_amt, transaction=transaction).save()
    elif data['Type'] == 'TOPUP':
        pass
    return transaction
