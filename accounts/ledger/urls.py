from django.urls import path

from . import views

urlpatterns = [
    path("coa.html", views.chart_of_accounts, name="coa"),
    path("import", views.import_csv, name="import_csv"),
]
