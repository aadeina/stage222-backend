from django_ratelimit.core import is_ratelimited
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from functools import wraps

# ✅ Custom handler that checks for rate limit and returns 429
def ratelimit_429(key: str, rate: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_ratelimited(
                request,
                key=key,
                rate=rate,
                method='POST',
                increment=True,
                group=f"ratelimit:{view_func.__name__}"
            ):
                return JsonResponse(
                    {"detail": "🚫 Too many requests. Please wait before retrying."},
                    status=429
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# 🔐 General authentication limits
def limit_login():
    return method_decorator(ratelimit_429(key='ip', rate='4/m'), name='dispatch')

def limit_register():
    return method_decorator(ratelimit_429(key='ip', rate='4/m'), name='dispatch')

def limit_change_password():
    return method_decorator(ratelimit_429(key='ip', rate='2/m'), name='dispatch')

def limit_verify_email():
    return method_decorator(ratelimit_429(key='ip', rate='2/m'), name='dispatch')

def limit_password_reset():
    return method_decorator(ratelimit_429(key='ip', rate='2/h'), name='dispatch')

def limit_password_reset_request():
    return method_decorator(ratelimit_429(key='ip', rate='2/h'), name='dispatch')

# ✅ Custom recruiter OTP limits
def limit_recruiter_send_otp():
    return ratelimit_429(key='ip', rate='2/m')  # Used as a decorator

def limit_recruiter_verify_otp():
    return ratelimit_429(key='ip', rate='3/m')  # Used as a decorator
