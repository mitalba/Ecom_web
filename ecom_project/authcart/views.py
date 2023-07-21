from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token  
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
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
                messages.info(request,"Email already Exists")
            #    return HttpResponse("Opps! Email Already Exists")
                return render(request,'signup.html')
            
        except Exception as e:
            pass
        
        user = User.objects.create_user(email,email,password)
        user.is_active = False
        user.save()
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,message,settings.EMAIL_HOST_USER,[email],
        )
        email.send()
        messages.success(request,"Activate Your Account by clicking the link on your gmail")
        return redirect('/auth/login/')

    return render(request,"signup.html")

class ActivateAccount(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as e:
            user = None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.info(request,"Account Activated")
            return redirect("/auth/login")
        return redirect(request,'auth/activatefail.html')

def handlelogin(request):
    return render(request,"login.html")

def handlelogout(request):
    return redirect('/auth/login')