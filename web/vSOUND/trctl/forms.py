from django import forms

class searchForm(forms.Form):
    search_text = forms.CharField(label='Suchen', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'type': 'text', 'placeholder': 'Suchen'}))
