from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'candidate'

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'recruiter'
