from django.shortcuts import render

# Create your views here.
# def index(request):

#     return render(request,"index.html")
def home(request):

    return render(request,"index.html")

def about(request):

    return render(request,"about.html")

def product(request):

    return render(request,"product.html")

def login(request):

    return render(request,"index.html")