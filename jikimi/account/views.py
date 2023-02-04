from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from violence_data_page.models import School
from django.contrib.auth.decorators import login_required


INVALID_PASSWORD = 0   #password 불일치
INVALID_EMAIL = 1
NO_SELECT_SCHOOL = 2

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
                                            user_school=School.objects.filter(school_id = request.POST['school_name'])[0],             # 셀렉트 박스...
                                            password=request.POST['password1']
                                            )
    
            # auth.login(redirect, user)
            return redirect("/")
        
        else:
            if(validate_code == INVALID_PASSWORD):
                return HttpResponse("<script>alert(\"비밀번호가 일치하지 않습니다.\");history.back();</script>")
            
            elif(validate_code == INVALID_EMAIL):
                return HttpResponse("<script>alert(\"이미 존재하는 이메일입니다.\");history.back();</script>")

            elif(validate_code == NO_SELECT_SCHOOL):
                return HttpResponse("<script>alert(\"학교를 선택해주세요.\");history.back();</script>")

    else:                                               # 학교 정보 출력
        school_info = School.objects.values("school_id", "school_name")
        list = {
            "schoolInfo" : school_info
        }
        return render(request, 'account/signup.html', list)
 
    return render(request, 'account/signup.html')

def isValidateUser(request):

    if(request.POST["password1"] != request.POST["password2"]):
        return INVALID_PASSWORD
    
    elif(request.POST["school_name"] == "0"):
        return NO_SELECT_SCHOOL

    elif(User.objects.filter(email = request.POST['email']).exists()):
        return INVALID_EMAIL
    
    return VALID_ACCOUNT

@login_required(login_url='account:login')
def my_page(request):
    return render(request, 'my_page/my_page.html')
