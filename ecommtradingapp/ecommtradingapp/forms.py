from django import forms

class RegisterForm(forms.Form):
    uname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    uemail = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)