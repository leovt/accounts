from django.contrib import admin

from .models import Classification, Currency, Account, Transaction, Entry, Period, ImportedEntry, ImportTask

admin.site.register(Currency)
admin.site.register(Period)
admin.site.register(Account)
admin.site.register(Classification)


class EntryInline(admin.TabularInline):
    model = Entry


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        EntryInline,
    ]

class ImportedEntryInline(admin.TabularInline):
    model = ImportedEntry

class ImportTaskAdmin(admin.ModelAdmin):
    inlines = [
        ImportedEntryInline,
    ]

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ImportTask, ImportTaskAdmin)
admin.site.register(ImportedEntry)