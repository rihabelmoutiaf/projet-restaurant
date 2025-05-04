from django.shortcuts import render , HttpResponse    
def home(request):   
  return render(request,'home.html')

def commander(request):   
  return render(request,'commander.html')
