
from django.shortcuts import render , HttpResponse 
def auth(request):   
  return render(request,'login.html')
