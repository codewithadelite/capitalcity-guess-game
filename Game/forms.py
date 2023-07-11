from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Country, Quiz


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('country_name', 'city_name')
        widgets = {
            'country_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_guest = True

        query = User.objects.filter(
            username=self.cleaned_data['username']).count()

        if(query < 1):

            user.save()
        return user
