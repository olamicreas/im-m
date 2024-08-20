from django.shortcuts import render, redirect
from .forms import Registration, CustomAuthenticationForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def signup(request):
	if request.method == 'POST':
		form = Registration(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/user/login')

	else:
		form = Registration()


	return render(request, 'users/signup.html', {'form': form, 'title': 'Sign Up'})


def Login(request):
	if request.method == 'POST':
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)

			if user is not None:

				login(request, user)
				return redirect('/user')

	else:
		form = CustomAuthenticationForm()

	return render(request, 'users/login.html', {'form': form, 'title': 'Login'})

def log_out(request):
    print('loggin out....')
    logout(request)
    
    return redirect('/user/login')



