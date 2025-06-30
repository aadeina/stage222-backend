from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.generics import get_object_or_404

from accounts.models import User
from candidates.models import CandidateProfile
from recruiters.models import RecruiterProfile
from internships.models import Internship
from applications.models import Application
from datetime import timedelta
from django.utils import timezone
from organizations.models import Organization


class PlatformStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        candidates = CandidateProfile.objects.all()
        recruiters = RecruiterProfile.objects.all()
        internships = Internship.objects.all()
        applications = Application.objects.all()

        internship_count = internships.count()
        application_count = applications.count()

        return Response({
            "users": {
                "total": users.count(),
                "verified": users.filter(is_verified=True).count(),
                "unverified": users.filter(is_verified=False).count(),
                "by_role": {
                    "candidate": users.filter(role="candidate").count(),
                    "recruiter": users.filter(role="recruiter").count(),
                    "admin": users.filter(role="admin").count()
                }
            },
            "candidates": {
                "total": candidates.count(),
                "with_resume": candidates.exclude(resume__isnull=True).exclude(resume__exact="").count(),
            },
            "recruiters": {
                "total": recruiters.count(),
                "verified_org": recruiters.filter(is_verified=True).count(),
                "unverified_org": recruiters.filter(is_verified=False).count(),
            },
            "internships": {
                "total": internship_count,
                "active": internship_count,  # Add 'status' support later
                "average_apps_per_post": round(application_count / internship_count, 2) if internship_count > 0 else 0
            },
            "applications": {
                "total": application_count,
                "pending": applications.filter(status="pending").count(),
                "accepted": applications.filter(status="accepted").count(),
                "rejected": applications.filter(status="rejected").count(),
                "shortlisted": applications.filter(shortlisted=True).count(),
            }
        })


class DailyGrowthSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Optional query params
        group_by = request.query_params.get("group", "day")  # default: day
        range_days = int(request.query_params.get("range", "30"))  # default: last 30 days
        since = timezone.now() - timedelta(days=range_days)

        # Determine group function
        if group_by == "week":
            trunc_func = TruncWeek
        elif group_by == "month":
            trunc_func = TruncMonth
        else:
            trunc_func = TruncDay

        user_growth = (
            User.objects.filter(created_at__gte=since)
            .annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        application_growth = (
            Application.objects.filter(created_at__gte=since)
            .annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        return Response({
            "user_growth": list(user_growth),
            "application_growth": list(application_growth)
        })

class TopInternshipsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        top_internships = (
            Internship.objects
            .annotate(application_count=Count("applications"))
            .order_by("-application_count")[:10]
        )

        data = [
            {
                "id": internship.id,
                "title": internship.title,
                "organization": internship.organization.name if internship.organization else None,
                "application_count": internship.application_count
            }
            for internship in top_internships
        ]

        return Response(data)
    

class TopRecruitersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        top_recruiters = (
            RecruiterProfile.objects
            .annotate(internship_count=Count("internships"))
            .order_by("-internship_count")[:10]
        )

        data = [
            {
                "user_id": recruiter.user.id,
                "full_name": f"{recruiter.first_name} {recruiter.last_name}",
                "email": recruiter.user.email,
                "organization": recruiter.organization.name if recruiter.organization else None,
                "internship_count": recruiter.internship_count
            }
            for recruiter in top_recruiters
        ]

        return Response(data)

from candidates.models import CandidateProfile, Skill
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

class TopSkillsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        skills = (
            Skill.objects
            .annotate(count=Count("candidates"))
            .order_by("-count")[:20]
        )

        data = [
            {
                "skill": skill.name,
                "count": skill.count
            }
            for skill in skills
        ]

        return Response(data)
    

class ShortlistRateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        internships = (
            Internship.objects
            .annotate(
                total_applications=Count("applications"),
                shortlisted_count=Count("applications", filter=Q(applications__shortlisted=True))
            )
            .filter(total_applications__gt=0)
            .order_by("-shortlisted_count")
        )

        data = []
        for internship in internships:
            shortlist_rate = (internship.shortlisted_count / internship.total_applications) * 100
            data.append({
                "internship_id": str(internship.id),
                "title": internship.title,
                "organization": internship.organization.name if internship.organization else None,
                "total_applications": internship.total_applications,
                "shortlisted": internship.shortlisted_count,
                "shortlist_rate": round(shortlist_rate, 2)
            })

        return Response(data)


class AdminUserListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        paginator = AdminUserListPagination()
        users = User.objects.all().order_by('-created_at')  # 🔁 FIXED here

        page = paginator.paginate_queryset(users, request)
        data = [
            {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "is_active": user.is_active,
                "date_joined": user.created_at
            }
            for user in page
        ]

        return paginator.get_paginated_response(data)

class AdminToggleVerifyUserView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        user.is_verified = not user.is_verified
        user.save()

        return Response({
            "id": str(user.id),
            "email": user.email,
            "is_verified": user.is_verified,
            "message": f"User has been {'verified' if user.is_verified else 'unverified'}."
        }, status=status.HTTP_200_OK)
    
class AdminToggleActiveUserView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        user.is_active = not user.is_active
        user.save()

        return Response({
            "id": str(user.id),
            "email": user.email,
            "is_active": user.is_active,
            "message": f"User has been {'activated' if user.is_active else 'deactivated'}."
        }, status=200)

class AdminDeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        email = user.email
        user.delete()
        return Response({
            "message": f"User {email} has been permanently deleted."
        }, status=200)

class AdminChangeUserRoleView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        new_role = request.data.get("role")

        # Validate input
        valid_roles = ['candidate', 'recruiter', 'admin']
        if new_role not in valid_roles:
            return Response({
                "error": "Invalid role. Choose from 'candidate', 'recruiter', or 'admin'."
            }, status=400)

        # Optional: prevent admins from changing their own role
        if user == request.user:
            return Response({
                "error": "You cannot change your own role."
            }, status=403)

        user.role = new_role
        user.save()

        return Response({
            "message": f"User role updated to '{new_role}'.",
            "user_id": str(user.id),
            "email": user.email,
            "new_role": user.role
        }, status=200)


class AdminPendingInternshipsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending_internships = Internship.objects.filter(approval_status='pending').order_by('-created_at')

        data = [
            {
                "id": str(intern.id),
                "title": intern.title,
                "organization": intern.organization.name if intern.organization else None,
                "recruiter_email": intern.recruiter.user.email,
                "submitted_on": intern.created_at,
                "status": intern.status,
                "approval_status": intern.approval_status
            }
            for intern in pending_internships
        ]

        return Response(data)
    

class AdminApproveInternshipView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        internship = get_object_or_404(Internship, id=id)

        if internship.approval_status == 'approved':
            return Response(
                {"message": "Internship is already approved."},
                status=status.HTTP_200_OK
            )

        internship.approval_status = 'approved'
        internship.rejection_reason = None  # Clear any past reason
        internship.save()

        return Response({
            "id": str(internship.id),
            "title": internship.title,
            "status": internship.status,
            "approval_status": internship.approval_status,
            "message": "Internship has been approved and is now visible."
        }, status=status.HTTP_200_OK)


class AdminRejectInternshipView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        internship = get_object_or_404(Internship, id=id)
        reason = request.data.get("reason", "").strip()

        if internship.approval_status == 'rejected':
            return Response(
                {"message": "Internship is already rejected."},
                status=status.HTTP_200_OK
            )

        internship.approval_status = 'rejected'
        internship.rejection_reason = reason if reason else None
        internship.save()

        return Response({
            "id": str(internship.id),
            "title": internship.title,
            "approval_status": internship.approval_status,
            "rejection_reason": internship.rejection_reason,
            "message": "Internship has been rejected."
        }, status=status.HTTP_200_OK)

# admin/views.py (or wherever your admin views are)

class AdminToggleVerifyOrganizationView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        org = get_object_or_404(Organization, id=id)
        org.is_verified = not org.is_verified
        org.save()

        return Response({
            "id": str(org.id),
            "name": org.name,
            "is_verified": org.is_verified,
            "message": f"✅ Organization has been {'verified' if org.is_verified else 'unverified'}."
        }, status=status.HTTP_200_OK)
