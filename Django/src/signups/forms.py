from django import forms
from models import SignUp

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = '__all__' # Or a list of the fields that you want to include in your form