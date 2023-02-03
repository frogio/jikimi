from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User


INVALID_PASSWORD = 0   #password 불일치
INVALID_EMAIL = 1

VALID_ACCOUNT = 9

validate_code = -1

def signup(request):

    global VALID_ACCOUNT, INVALID_EMAIL, INVALID_PASSWORD
    global validate_code    
    
    if(request.method == "POST"):               # POST
        
        validate_code = isValidateUser(request)
        
        if(validate_code == VALID_ACCOUNT):             # 유효성 검사
            user = User.objects.create_user(
                                            username = request.POST['email'],
                                            email=request.POST['email'],
                                            user_phone = request.POST['phone_no'],
                                            # user_school=None,
                                            password=request.POST['password1']
                                            )
    
            # auth.login(redirect, user)
            return redirect("/")
        
        else:
            if(validate_code == INVALID_PASSWORD):
                return HttpResponse("<script>alert(\"비밀번호가 일치하지 않습니다.\");history.back();</script>")
            
            elif(validate_code == INVALID_EMAIL):
                return HttpResponse("<script>alert(\"이미 존재하는 이메일입니다.\");history.back();</script>")
    
    return render(request, 'account/signup.html')

def isValidateUser(request):

    if(request.POST["password1"] != request.POST["password2"]):
        return INVALID_PASSWORD
    
    if(User.objects.filter(email = request.POST['email']).exists()):
        return INVALID_EMAIL
    
    return VALID_ACCOUNT
