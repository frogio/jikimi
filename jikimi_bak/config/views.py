from django.shortcuts import render
# Create your views here.

def index(request):	
    return render(request, 'main_page/main.html')
	# context 딕셔너리는 템플릿으로 넘어가 키 값으로 데이터를 참조할 수 있다.