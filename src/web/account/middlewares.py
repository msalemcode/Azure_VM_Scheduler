from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from urllib.parse import urlencode
from .exceptions import AuthError

class HandleAuthErrorMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, AuthError):
            query_string =  urlencode({
                'type': exception.__class__.__name__,
                'message': exception.message,
            })
            return redirect('/account/error?' + query_string)
            