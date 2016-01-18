from django.http import HttpResponse


def index(request):
    a = None
    # a purposeful error
    a.__dict__
    return HttpResponse("Hello, world. You're at the polls index.")
