# Generated by Django 4.2.7 on 2023-12-09 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0005_transaction_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedentry',
            name='account_hint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ledger.account'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='entries', to='ledger.account'),
        ),
    ]
