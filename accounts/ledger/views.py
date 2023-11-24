import csv
import io

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Account, Classification

class Bag:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def chart_of_accounts(request):
    unclassified = set(account.number for account in Account.objects.all())
    seen = set()
    todo = [("Root", 0)]
    rows = []
    while todo:
        cid, level = todo.pop()
        if cid in seen:
            #TODO: add warning
            continue
        seen.add(cid)
        classification = Classification.objects.get(id=cid)
        todo.extend(reversed([(x.id, level+1) for x in classification.children.all()]))
        rows.append(Bag(level=level, name=str(classification)))
        for account in classification.account_set.all():
            rows.append(account)
            unclassified.discard(account.number)
    if unclassified:
        rows.append(Bag(level=0, name="Unclassified"))
        rows.extend(account for account in Account.objects.all() if account.number in unclassified)
    return render(request, "ledger/coa.html", {'rows':rows})

def import_csv(request):
    from .forms import UploadFileForm
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES["file"].read().decode('utf-8')
            filename = request.FILES["file"].name
            print(filename)
            reader = csv.DictReader(io.StringIO(content))
            for line in reader:
                print(line)
                break
            #return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "ledger/upload.html", {"form": form})

def import_task(request):
    pass
