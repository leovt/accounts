from django.contrib import admin

from .models import Classification, Currency, Account, Transaction, Entry

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Classification)


class EntryInline(admin.TabularInline):
    model = Entry


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]

admin.site.register(Transaction, TransactionAdmin)
