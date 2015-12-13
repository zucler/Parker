from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. We are at the carparker index")
