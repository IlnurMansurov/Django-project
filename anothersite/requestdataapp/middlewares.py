
from django.http import HttpRequest
from django.http import HttpResponseForbidden
import time
def set_useragent_on_request_middleware(get_response):
    print('initial call')

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests_count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('response_count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')





class ThrottlingMiddleware:
    """
    Middleware для ограничения обработки запросов пользователя в зависимости от его IP-адреса.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        if ip_address in self.requests:
            last_request = self.requests[ip_address]
            if time.time() - last_request < 0.001:
                return HttpResponseForbidden('Слишком много запросов. Пожалуйста, попробуйте еще раз позже.')
        self.requests[ip_address] = time.time()
        response = self.get_response(request)
        return response