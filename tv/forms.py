from django import forms

from users.models import Group


class GroupRegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    about = forms.CharField(max_length=200)


class GroupUpdateForm(forms.ModelForm):
    name = forms.TextInput()
    about = forms.TextInput()

    class Meta:
        model = Group
        fields = ['name', 'about', 'image']

