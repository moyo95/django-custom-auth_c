from django import forms
from allauth.account.forms import SignupForm


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    address = forms.CharField(max_length=30, label='住所', required=False)
    tel = forms.CharField(max_length=30, label='電話番号', required=False)

class SignupUserForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')

    def dave(self, request):
        user = super(SignupUserForm, self).seve(request)
        user.first_name = self.cleand_data['first_name']
        user.lastt_name = self.cleand_data['last_name']
        user.seve()
        return user
