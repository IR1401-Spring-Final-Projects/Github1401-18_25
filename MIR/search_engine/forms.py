from django import forms


class InputForm(forms.Form):
    input = forms.CharField(label='Input', widget=forms.Textarea())
    expansion = forms.BooleanField(label='expansion',  required=False)