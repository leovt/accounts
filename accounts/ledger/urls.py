from django.urls import path

from . import views

urlpatterns = [
    path("coa.html", views.chart_of_accounts, name="coa"),
    path("import", views.import_csv, name="import_csv"),
    path("import/<int:task_id>", views.import_task, name="import_task"),
    path("import_transaction/<int:import_entry_id>", views.import_transaction, name="import_transaction"),
    path("transaction/<int:transaction_id>", views.transaction, name="transaction"),
    path("balances/<str:period_id>", views.balances, name="balances"),
]
