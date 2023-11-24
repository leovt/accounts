from django.db import models

class Currency(models.Model):
    class Meta:
        verbose_name_plural = "currencies"
    code = models.CharField(max_length=3, primary_key=True)

class Classification(models.Model):
    class Meta:
        ordering = ["id"]
    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    parent = models.ForeignKey("self", on_delete=models.RESTRICT, related_name="children")

    def __str__(self):
        return f"{self.id} - {self.name}"

class Account(models.Model):
    class Meta:
        ordering = ["number"]
    number = models.CharField(max_length=10, primary_key=True)
    short_name = models.CharField(max_length=30, unique=True, null=False, blank=False)
    long_name = models.CharField(max_length=100, null=False, blank=True)
    classification = models.ForeignKey(Classification, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.number} - {self.short_name}"

class Transaction(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    source = models.CharField(max_length=200)
    def __str__(self):
        return self.description

class ImportTask(models.Model):
    source = models.CharField(max_length=200)


class ImportedEntry(models.Model):
    class Meta:
        ordering = ["task", "serial"]
        unique_together = [["task", "serial"]]
    task = models.ForeignKey(ImportTask, on_delete=models.CASCADE)
    serial = models.IntegerField()
    data = models.JSONField()
    transaction = models.ForeignKey(Transaction, null=True, on_delete=models.SET_NULL)


class Entry(models.Model):
    DEBIT = "DR"
    CREDIT = "CR"

    transaction = models.ForeignKey(Transaction, null=False, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=False, on_delete=models.RESTRICT)
    currency = models.ForeignKey(Currency, null=False, on_delete=models.RESTRICT, related_name='+')
    etype = models.CharField(max_length=2, blank=False, null=False,
        choices = ((DEBIT, "Debit"), (CREDIT, "Credit")))
    amount = models.DecimalField(max_digits=16, decimal_places=4)