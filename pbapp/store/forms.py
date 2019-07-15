from django import forms
from django.forms.utils import ErrorList



class Register(forms.Form):
    name = forms.CharField(
        label='name',
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-group', 'placeholder':'Nom'}),
        required=True,

    )
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={'class':'form-group', 'placeholder':'Email'}),
        required=True
    )
    passwd = forms.CharField(
        label='passwd',
        widget=forms.PasswordInput(),
        required=True
    )


class searchProduct(forms.Form):
    search = forms.CharField(
        label='search',
        widget=forms.TextInput(attrs={'class':'form-inline'}),
        required=False
    )

class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])