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
                group=f"ratelimit:{view_func.__name__}"  # 👈 REQUIRED
            ):
                return JsonResponse(
                    {"detail": "🚫 Too many requests. Please wait before retrying."},
                    status=429
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# 🔐 Per-view method decorators for consistency and UX-friendly feedback
def limit_login():
    return method_decorator(ratelimit_429(key='ip', rate='5/m'), name='dispatch')


def limit_register():
    return method_decorator(ratelimit_429(key='ip', rate='5/m'), name='dispatch')


def limit_change_password():
    return method_decorator(ratelimit_429(key='ip', rate='3/m'), name='dispatch')


def limit_verify_email():
    return method_decorator(ratelimit_429(key='ip', rate='3/m'), name='dispatch')


def limit_password_reset():
    return method_decorator(ratelimit_429(key='ip', rate='3/h'), name='dispatch')


def limit_password_reset_request():
    return method_decorator(ratelimit_429(key='ip', rate='3/h'), name='dispatch')
