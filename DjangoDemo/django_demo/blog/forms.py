from django import forms
from blog.models import Users
from django.conf import settings

# Create your forms here.

class SignupForm (forms.Form):
    email = forms.EmailField( error_messages={'required': 'This field is required!','invalid':'Wrong formation!'},
        label='Email Address',required=True,widget=forms.EmailInput(attrs={'placeholder':'Please type in your email address!'}))
    password =forms.CharField( error_messages={'required': 'This field is required!'},
        label='Password',required=True,max_length=20,widget = forms.PasswordInput(attrs={'placeholder':'Please create a password for ur account!'}))
    confirm_password= forms.CharField(error_messages={'required': 'This field is required!'},
        label='Re-password',required=True,max_length=20,min_length=6,widget = forms.PasswordInput(attrs={'placeholder':'Please type in your password again!'}))
    
    class Meta:
        model = Users
        fields = ['userID', 'emailAddress', 'password']

    def getEmail(self):
        breakpoint()
        print(self.email)
        return self.email