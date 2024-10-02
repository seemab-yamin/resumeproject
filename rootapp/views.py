from django.shortcuts import render


def root(request):
    return render(request, "rootapp/index.html", {"submitted": False})
