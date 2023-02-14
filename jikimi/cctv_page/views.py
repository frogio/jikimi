from django.shortcuts import render
from .models import Video
from django.contrib.auth.decorators import login_required


@login_required(login_url='account:login')
def cctv_page(request):	
    videoList = Video.objects.filter(video_school = request.user.user_school)    
    
    list = {
        "videoList" : videoList 
    }

    url = request.GET.get("video_url")

    if(url != None):
        list['video_url'] = url
    
    return render(request, 'cctv_page/cctv.html', list)

