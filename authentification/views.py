from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def auth(request):
    error = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Identifiants invalides."  

    return render(request, 'login.html', {'error': error})
