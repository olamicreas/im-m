from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Registration(UserCreationForm):
	email = forms.EmailField(required=True, max_length=254, help_text='Required. Enter a valid email address.', widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}))


	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control'})


	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data.get('email')
		if commit:
			user.save()


		return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

