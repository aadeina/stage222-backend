from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

def limit_login():
    return method_decorator(
        ratelimit(key='ip', rate='5/m', method='POST', block=True),
        name='dispatch'
    )

def limit_register():
    return method_decorator(
        ratelimit(key='ip', rate='5/m', method='POST', block=True),
        name='dispatch'
    )

def limit_change_password():
    return method_decorator(
        ratelimit(key='ip', rate='3/m', method='POST', block=True),
        name='dispatch'
    )

def limit_verify_email():
    return method_decorator(
        ratelimit(key='ip', rate='3/m', method='POST', block=True),
        name='dispatch'
    )
