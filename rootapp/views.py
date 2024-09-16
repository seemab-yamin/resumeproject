from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from rootapp.forms import ContactForm
# Create your views here.


def root(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "website_inquiry"
            body = {
                "name": form.cleaned_data["full_name"],
                "email": form.cleaned_data["email"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(
                    subject, message, "seemab.y1@gmail.com", ["seemab.y1@gmail.com"]
                )
            except BadHeaderError:
                return HttpResponse("Invalid Header Found.")
            form = ContactForm()
            # return redirect('/#foot', {'submitted' : True})
            return render(request, "rootapp/index.html", {"submitted": True})
    form = ContactForm()
    return render(request, "rootapp/index.html", {"form": form, "submitted": False})
