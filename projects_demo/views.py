from django.shortcuts import render


# Create your views here.
def projects_demo(request):
    return render(request, "projects_demo/index.html")
