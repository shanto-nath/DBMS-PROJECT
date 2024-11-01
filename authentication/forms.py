from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES, label='User Type')

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password', 'confirm_password', 'nid', 'user_type']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_confirm_password(self):
        specialSym = ["$", "@", "#", "%", "*", "^", "!"]
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        if len(password) <= 7:
            raise forms.ValidationError("Password must be at least 8 characters long")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must have at least one digit")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must have at least one uppercase letter")
        
        if not any(char in specialSym for char in password):
            raise forms.ValidationError("Password must have at least one special character")
        
        return confirm_password
    
    def clean_nid(self):
        nid = self.cleaned_data.get('nid')
        if UserProfile.objects.filter(nid=nid).exists():
            raise forms.ValidationError('This NID number is already in use.')
        return nid

    def save(self, commit=True):
        # Save user profile with user_type
        user_profile = super().save(commit=False)
        user_profile.user_type = self.cleaned_data['user_type']
        if commit:
            user_profile.save()
        return user_profile


class SignInForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Invalid email or password. Please try again."
        ),
    }
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'contact_no', 'gender', 'nid', 'dob', 'address', 'profile_picture']  # Include only necessary fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget = forms.DateInput(attrs={'type': 'date'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email already Exists")
        
        return email   