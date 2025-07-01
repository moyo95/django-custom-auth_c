from django import forms

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    postal_code = forms.CharField(max_length=7, label='郵便番号', required=False)
    address1 = forms.CharField(max_length=255, label='住所1', required=False)
    address2 = forms.CharField(max_length=255, label='住所2', required=False)
    tel = forms.CharField(max_length=30, label='電話番号', required=False)
    first_name_kana = forms.CharField(max_length=30, label='姓のふりがな', required=False)
    last_name_kana = forms.CharField(max_length=30, label='名のふりがな', required=False)