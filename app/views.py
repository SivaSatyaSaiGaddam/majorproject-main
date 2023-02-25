from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"home.html")

def register(request):
    return render(request,"register.html")

def attendance(request):
    return render(request,"attendnace.html")

def show(request):
    return render(request,"show.html")
