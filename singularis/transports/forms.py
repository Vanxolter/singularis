from django import forms


class TransportsForm(forms.Form):
    feet = forms.BooleanField(required=False)
    auto = forms.BooleanField(required=False)
    train = forms.BooleanField(required=False)
    fly = forms.BooleanField(required=False)