from django.http import HttpResponseServerError, HttpResponseNotAllowed

class Http505Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'HTTP_VERSION' in request.META and \
           request.META['HTTP_VERSION'] not in ('HTTP/1.1', 'HTTP/2'):
            return custom_505_view(request)
        return response