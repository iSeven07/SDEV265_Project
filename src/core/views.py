from django.shortcuts import render
#test
# Create your views here.
def home(request):
    print(request.headers)
    return render(request, "home.html", {})