from django.shortcuts import render


def menu(request):   
    return render(request, 'menu.html')

def about(request):   
    return render(request, 'about.html')
