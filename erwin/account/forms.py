from django.contrib.auth.forms import UserCreationForm , AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, EmailInput, PasswordInput


#Registration Form

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)


        #mark email field as required
        self.fields['email'].required = True

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    #Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        if len(email) >= 300:
            raise forms.ValidationError("Your email is too long.")
        return email
    

#Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#Update form
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        exclude = ['password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)


        #mark email field as required
        self.fields['email'].required = True

    #Email Validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk =self.instance.pk).exists():
            raise forms.ValidationError("Email is already in use.")
        if len(email) >= 300:
            raise forms.ValidationError("Your email is too long.")
        return email

    

    
    