from rest_framework.permissions import BasePermission

# ✅ Candidate-only access
class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'candidate' and
            hasattr(request.user, 'candidate')
        )

# ✅ Recruiter-only access
class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'recruiter' and
            hasattr(request.user, 'recruiter')
        )

# ✅ Admin-only access
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
