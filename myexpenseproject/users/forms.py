from django import forms

class ItemCreationForm(forms.Form):
    item_name = forms.CharField(max_length=25)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()