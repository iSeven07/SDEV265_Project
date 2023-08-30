from django.shortcuts import render

# Create your views here.
def home(request):
    print(request.headers)
    return render(request, "home.html", {})