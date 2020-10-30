from django.shortcuts import render

# Create your views here.
def index(request):
	context = locals()
	return render(request,'Blog/index.html', context)