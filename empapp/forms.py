from django import forms
from django.contrib.auth.models import Group, User
from .models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-field form-group mt-3 col-md-3 bg-light', 'placeholder': "Enter Password..."}))
    role = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-group col-md-2 mb-3 form_field', }),
                                  queryset=Group.objects.all())
    gender = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-group col-md-2 mb-3 form_field', }),
                                    queryset=Group.objects.all())
    department = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-field form-group col-md-5 form_field'}),
        queryset=Department.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'gender', 'role', 'email', 'department']
        help_texts = {
            'username': None,
            'email': None,
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control col-md-3 bg-light form-field', 'placeholder': "Enter First Name..."}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control col-md-3 bg-light form-field', 'placeholder': "Enter Last Name..."}),
            'username': forms.TextInput(
                attrs={'class': 'form-group col-md-3 bg-light form-field', 'placeholder': "Enter User Name..."}),
            'email': forms.TextInput(attrs={'class': 'form-control col-md-8 mb-2 bg-light form-field',
                                            'placeholder': 'Enter Your Email Address ..'}),

        }


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 bg-light m-auto'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-md-6 bg-light m-auto'}))


class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask

        fields = '__all__'
        exclude = ['date', 'user']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['from_date', 'to_date', 'cause_of_leave']

        widgets = {

            'from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'cause_of_leave': forms.Textarea(attrs={'class': 'form-control'})
        }


class PunchInForm(forms.ModelForm):
    class Meta:
        model = PunchIn

        fields = ['In_Note']
        exclude = ['user']

        widgets = {
            'In_Note': forms.TextInput(attrs={'class': 'form-control col-md-6 mb-2'}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-md-2 bg-light m-auto'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-md-2 bg-light m-auto'}))
