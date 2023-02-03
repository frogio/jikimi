from django.shortcuts import render
from .models import Video
from django.contrib.auth.decorators import login_required


@login_required(login_url='account:login')
def cctv_page(request):	
    videoList = Video.objects.all()    
    
    list = {
        "videoList" : videoList 
    }

    return render(request, 'cctv_page/cctv.html', list)

