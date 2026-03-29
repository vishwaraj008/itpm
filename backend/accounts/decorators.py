from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(*roles):
    """Decorator to restrict views to specific user roles."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not hasattr(request.user, 'userprofile'):
                return HttpResponseForbidden("No profile found.")
            if request.user.userprofile.role not in roles:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You do not have permission to access this page.</p>"
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Shortcut decorator for admin-only views."""
    return role_required('admin')(view_func)


def faculty_or_admin_required(view_func):
    """Shortcut decorator for faculty/admin views."""
    return role_required('faculty', 'admin')(view_func)
