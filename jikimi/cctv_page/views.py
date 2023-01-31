from django.shortcuts import render
from .models import Video


def cctv_page(request):	
    videoList = Video.objects.all()    
    
    list = {
        "videoList" : videoList 
    }

    return render(request, 'cctv_page/cctv.html', list)

