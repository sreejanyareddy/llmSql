from django import forms

class QueryForm(forms.Form):
    user_text = forms.CharField(label="Enter Query", max_length=255)
    temperature = forms.FloatField(initial=0.7)
    db_schema = forms.CharField(widget=forms.Textarea)
