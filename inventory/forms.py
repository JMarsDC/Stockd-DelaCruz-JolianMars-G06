from django import forms

from .models import Storage


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ("name", "storage_type", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Storage name must be at least 2 characters.")
        duplicates = Storage.objects.filter(owner=self.user, name__iexact=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("You already have a storage with this name.")
        return name