from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from pages.models import Currency
import re
from users.encryption_util import load_key, encrypt_data, decrypt_data


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'fullName'}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
        error_messages={'required': 'Це поле обов\'язкове.', 'invalid': 'Введіть коректну електронну пошту (повинні бути символи @ та .).'}
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'currency'}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'photo', 'accept': 'image/*', 'onchange': 'previewPhoto()'})
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'currency', 'photo', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
        }
        error_messages = {
            'username': {'required': 'Це поле обов\'язкове.'}
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ця адреса електронної пошти вже використовується.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise forms.ValidationError('Логін може містити тільки англійські літери, цифри та символи _ або -.')
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Пароль повинен містити щонайменше 8 символів.')
        if not re.search(r'[A-Za-z]', password1):
            raise forms.ValidationError('Пароль повинен містити хоча б одну літеру.')
        if not re.search(r'\d', password1):
            raise forms.ValidationError('Пароль повинен містити хоча б одну цифру.')
        if not re.search(r'[@$!%*?&]', password1):
            raise forms.ValidationError('Пароль повинен містити хоча б один спеціальний символ (@$!%*?&).')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            key = load_key('users/encryption_key.key')
            encrypted_password = encrypt_data(self.cleaned_data['password1'], key)
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                currency=self.cleaned_data['currency'],
                photo=self.cleaned_data.get('photo'),
                encrypted_password=encrypted_password
            )
        return user
    

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'login',
            'required': True
        }),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'required': True
        }),
        error_messages={'required': 'Це поле обов\'язкове.'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Даного логіну не існує")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                key = load_key('users/encryption_key.key')
                decrypted_password = decrypt_data(profile.encrypted_password, key)
                
                if password != decrypted_password:
                    self.add_error('password', "Неправильний пароль")
            except User.DoesNotExist:
                raise forms.ValidationError("Даного логіну не існує")
            except Profile.DoesNotExist:
                raise forms.ValidationError("Профіль не знайдено")

        return cleaned_data



class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    password1 = forms.CharField(
        label="Новий пароль",
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'})
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'currency', 'photo', 'username', 'email', 'password1', 'password2']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'fullName'}),
            'currency': forms.Select(attrs={'class': 'form-select', 'id': 'currency'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'photo', 'accept': 'image/*', 'onchange': 'previewPhoto()'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('username', "Користувач з таким логіном вже існує.")
        return username


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            self.add_error('password2', "Паролі не співпадають")

        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password1']:
            key = load_key('users/encryption_key.key')
            encrypted_password = encrypt_data(self.cleaned_data['password1'], key)
            profile.encrypted_password = encrypted_password
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            profile.save()
        return profile
