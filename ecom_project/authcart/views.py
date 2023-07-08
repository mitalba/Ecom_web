from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request,"Password Is Not Matching")
            # return HttpResponse('Opps! /Password Is Incorrect')
            return render(request,'signup.html')
        
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email already Exists")
            #    return HttpResponse("Opps! Email Already Exists")
                return render(request,'signup.html')
            
        except Exception as e:
            pass
        
        user = User.objects.create_user(email,email,password)
        user.save()
        return HttpResponse(email,"user created")
    return render(request,"signup.html")

def handlelogin(request):
    return render(request,"login.html")

def handlelogout(request):
    return redirect('/auth/login')