from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")


def contact_us(request):
    return render(request,"contact.html")

def about_us(request):
    return render(request,"about.html")