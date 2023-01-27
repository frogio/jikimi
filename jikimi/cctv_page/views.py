from django.shortcuts import render
from .models import Video 


# Create your views here.
def cctv_page(request):	
    videoList = Video.objects.all()    
    
    list = {
        "videoList" : videoList 
    }

    return render(request, 'cctv_page/cctv.html', list)
	# context 딕셔너리는 템플릿으로 넘어가 키 값으로 데이터를 참조할 수 있다.