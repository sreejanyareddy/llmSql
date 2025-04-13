from django import forms

class QueryFormWithSchema(forms.Form):
    user_text = forms.CharField(label="Enter Query", max_length=4095)
    temperature = forms.FloatField(initial=0.7)
    db_schema = forms.CharField(widget=forms.Textarea)

class QueryFormWithoutSchema(forms.Form):
    user_text = forms.CharField(label="Enter Query", max_length=4095)
    temperature = forms.FloatField(initial=0.7)
