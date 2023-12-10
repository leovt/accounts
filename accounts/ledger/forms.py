from django import forms

from .models import Entry, Transaction

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def _formfield_for_dbfield(db_field, **kwargs):
    if db_field.name == "transaction":
        return db_field.formfield(widget=forms.HiddenInput, disabled=True, **kwargs)
    return db_field.formfield(**kwargs)
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['etype','account','amount','currency','transaction']
        formfield_callback = _formfield_for_dbfield

EntryFormSet = forms.modelformset_factory(Entry, form=EntryForm, extra=2, max_num=10)
