from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def error_404_view(request, exception):
    return render(request, '404.html')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['email'] and request.POST['password']:
                email = request.POST['email']
                password = request.POST['password']
                username = User.objects.filter(email = email).values()
                if username:
                    username_1 = username[0]['username']
                    user = authenticate(request, username = username_1, password = password)
                    if user is not None:
                        auth.login(request, user)
                        if request.POST['next'] != '':
                            return redirect(request.POST.get('next'))
                        else:
                            return redirect('/')
                    else:
                        return render(request, 'login.html', {'error': 'Invalid Credentials'})
                else:
                    return render(request, 'login.html', {'error': 'User Does not Exist'})
            else:
                return render(request, 'login.html', {'error': "Empty Fields"})
        else:
            return render(request, 'login.html')
    else:
        return redirect('/')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['username'] and request.POST['email'] and request.POST['password'] and request.POST['password2']:
                if request.POST['password'] == request.POST['password2']:
                    if not User.objects.filter(email = request.POST['email']).exists() and not User.objects.filter(username = request.POST['username']).exists():
                        user = User.objects.create_user(
                            username=request.POST['username'],
                            email=request.POST['email'],
                            password=request.POST['password'],
                        )
                        user.save()
                        messages.success(
                            request, "Signup Successful! Login Here")
                        return redirect(login)
                    else:
                        return render(request, 'signup.html', {'error': "Username or Email Already Taken"})
                else:
                    return render(request, 'signup.html', {'error': "Password's Don't Match"})
            else:
                return render(request, 'signup.html', {'error': "Empty Fields"})
        else:
            return render(request, 'signup.html')
    else:
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/login')