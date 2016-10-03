from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from libapp.models import Suggestion,Book,Dvd,Libitem,User,Libuser

class SuggestionForm(forms.ModelForm):
    class Meta:
        model=Suggestion
        fields = ['title','pubyr','type','cost','comments']
        widgets = {
            'type':forms.RadioSelect(),
        }
        labels = {
            'pubyr':u'Year of publication',
            'cost':u'Estimated cost in Dollars',
        }

    default_error_messages = {
        'max_length':(u'Ensure this value has at most %(max)d characters (it has %(length)d).'),
        'min_length':(u'Ensure this value has at least %(min)d characters (it has %(length)d).'),
    }
    pubyr=forms.IntegerField(error_messages=default_error_messages,validators=[MaxValueValidator(2016), MinValueValidator(1900)])

class SearchlibForm(forms.ModelForm):
    class Meta:
        model=Libitem
        fields=['title']
    title=forms.CharField(max_length=100,required=False)
    by=forms.CharField(max_length=100,required=False)

class LoginForm(forms.Form):
    class Meta:
        fields=['username','password']
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100,widget=forms.PasswordInput)

class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username']

class RegisterForm(forms.ModelForm):
    class Meta:
        model=Libuser
        fields=['first_name','last_name','email','username','password','address','city','postalcode','province','phone','profile_image']
        widgets={
            'province':forms.Select(),
        }
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    address = forms.Textarea()
    city = forms.CharField(max_length=30, required=True,initial='Windsor')
    postalcode = forms.CharField(max_length=7, required=False)
    phone=forms.CharField(max_length=11,required=False)
    profile_image=forms.ImageField(required=False)

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Libuser
        fields=['first_name','last_name','email','address','city','postalcode','province','phone','profile_image']
        exclude=['usrname','password']
        widgets = {
            'province': forms.Select(),
        }
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    address = forms.Textarea()
    city = forms.CharField(max_length=30, required=True)
    postalcode = forms.CharField(max_length=7, required=False)
    phone = forms.CharField(max_length=11, required=False)
    profile_image = forms.ImageField(required=False)
