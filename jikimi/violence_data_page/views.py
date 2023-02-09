from django.shortcuts import render, get_object_or_404
from violence_data_page.models import SchoolData 
from django.contrib.auth.decorators import login_required

# 고등학교 이름
# school_data_school(FK) 

# 시군구 / 환경지표 / 위해지표 / 경감지표 / 총 점수 / 학교폭력 위험도
# region_name / region_environment_score / school_data_harzard / school_alleviate /  school_total_score / school_data_degree

# Create your views here.

@login_required(login_url='account:login')
def violence_data_page(request):	
    school_harzard = get_object_or_404(SchoolData, pk = request.user.user_school.school_id)
    
    school_harzard.school_data_school.school_address1.region_environment_score = round(school_harzard.school_data_school.school_address1.region_environment_score)
    school_harzard.school_data_total_score = round(school_harzard.school_data_total_score)

    info = {
        "schoolInfo" : school_harzard 
    }

    return render(request, 'violence_data/violence_data.html', info)    
