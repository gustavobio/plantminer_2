from django import forms

# class AutoCompleteForm(forms.Form):
#     auto_complete = forms.TextInput(required=True, widget=forms.TextInput(
#         attrs={
#             'style': 'width: 400px',
#             'class': 'basicAutoComplete',
#             'data-url': "/api/autocomplete/"
#         }))

class ListForm(forms.Form):
    list = forms.CharField(widget=forms.Textarea, label = "Paste your taxa, one in each line:")
    suggest = forms.BooleanField(widget=forms.CheckboxInput, label = 'Suggest corrections for misspelled names', required = False)
    replace_synonyms = forms.BooleanField(widget=forms.CheckboxInput, label = 'Automatically replace synonyms', required = False)