import csv
import io

from django.shortcuts import render, get_object_or_404, redirect

from .models import Account, Classification, ImportTask, ImportedEntry

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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
            reader = csv.DictReader(io.StringIO(content))
            task = ImportTask(source=filename, fieldnames=reader.fieldnames)
            from django.db import transaction
            with transaction.atomic():
                task.save()
                for serial, data in enumerate(reader):
                    entry = ImportedEntry(task=task, serial=serial, data=data)
                    entry.save()
            return redirect('import_task', task.id)
    else:
        form = UploadFileForm()
    return render(request, "ledger/upload.html", {"form": form})

def import_task(request, task_id):
    task = get_object_or_404(ImportTask, id=task_id)
    return render(request, "ledger/importtask.html", {
        'source':task.source,
        'fieldnames':task.fieldnames,
        'entries': [x.data for x in task.entries.all()],
    })
