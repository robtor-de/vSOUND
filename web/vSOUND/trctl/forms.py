from django import forms

class searchForm(forms.Form):
    search_text = forms.CharField(label='Suchen', max_length=30)
