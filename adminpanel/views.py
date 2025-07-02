from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdminRole
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from candidates.models import CandidateProfile
from recruiters.models import RecruiterProfile
from internships.models import Internship
from applications.models import Application
from organizations.models import Organization

from adminpanel.permissions import IsAdminRole



class PlatformStatsView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        # USERS
        users = User.objects.all()
        total_users = users.count()
        verified_users = users.filter(is_verified=True).count()
        unverified_users = total_users - verified_users

        # ROLES
        roles = {
            "candidate": users.filter(role="candidate").count(),
            "recruiter": users.filter(role="recruiter").count(),
            "admin": users.filter(role="admin").count(),
        }

        # CANDIDATES
        candidates = CandidateProfile.objects.all()
        candidates_with_resume = candidates.exclude(resume__isnull=True).exclude(resume__exact="").count()

        # RECRUITERS
        recruiters = RecruiterProfile.objects.all()
        verified_recruiters = recruiters.filter(is_verified=True).count()
        unverified_recruiters = recruiters.filter(is_verified=False).count()

        # ORGANIZATIONS
        organizations = Organization.objects.all()
        total_orgs = organizations.count()
        verified_orgs = organizations.filter(is_verified=True).count()
        unverified_orgs = total_orgs - verified_orgs

        # INTERNSHIPS
        internships = Internship.objects.all()
        internship_count = internships.count()

        # Applications
        applications = Application.objects.all()
        application_count = applications.count()
        apps_per_post = round(application_count / internship_count, 2) if internship_count else 0

        return Response({
            "users": {
                "total": total_users,
                "verified": verified_users,
                "unverified": unverified_users,
                "by_role": roles
            },
            "candidates": {
                "total": candidates.count(),
                "with_resume": candidates_with_resume
            },
            "recruiters": {
                "total": recruiters.count(),
                "verified": verified_recruiters,
                "unverified": unverified_recruiters
            },
            "organizations": {
                "total": total_orgs,
                "verified": verified_orgs,
                "unverified": unverified_orgs
            },
            "internships": {
                "total": internship_count,
                "active": internship_count,  # update once status is added
                "average_apps_per_post": apps_per_post
            },
            "applications": {
                "total": application_count,
                "pending": applications.filter(status="pending").count(),
                "accepted": applications.filter(status="accepted").count(),
                "rejected": applications.filter(status="rejected").count(),
                "shortlisted": applications.filter(shortlisted=True).count()
            }
        })

class DailyGrowthSummaryView(APIView):
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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



class TopSkillsView(APIView):
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        email = user.email
        user.delete()
        return Response({
            "message": f"User {email} has been permanently deleted."
        }, status=200)

class AdminChangeUserRoleView(APIView):
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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
    permission_classes = [IsAdminRole]

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

class AdminGrowthTrendsView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        group_by = request.query_params.get("group", "day")
        range_days = int(request.query_params.get("range", "30"))
        since = timezone.now() - timedelta(days=range_days)

        trunc = {"day": TruncDay, "week": TruncWeek, "month": TruncMonth}.get(group_by, TruncDay)

        recruiter_growth = (
            RecruiterProfile.objects.filter(created_at__gte=since)
            .annotate(period=trunc("created_at"))
            .values("period")
            .annotate(count=Count("id")).order_by("period")
        )

        internship_growth = (
            Internship.objects.filter(created_at__gte=since)
            .annotate(period=trunc("created_at"))
            .values("period")
            .annotate(count=Count("id")).order_by("period")
        )

        org_growth = (
            Organization.objects.filter(created_at__gte=since)
            .annotate(period=trunc("created_at"))
            .values("period")
            .annotate(count=Count("id")).order_by("period")
        )

        return Response({
            "recruiter_growth": list(recruiter_growth),
            "internship_growth": list(internship_growth),
            "organization_growth": list(org_growth)
        })

class AdminEngagementMetricsView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        now = timezone.now()
        last_24h = now - timedelta(days=1)
        last_30d = now - timedelta(days=30)

        # DAU / MAU
        daily_active_users = User.objects.filter(last_login__gte=last_24h).count()
        monthly_active_users = User.objects.filter(last_login__gte=last_30d).count()

        # Candidate profile completion
        candidates = CandidateProfile.objects.all()
        profile_completed = candidates.exclude(resume='').filter(skills__isnull=False).distinct().count()
        total_candidates = candidates.count()
        completion_rate = round((profile_completed / total_candidates) * 100, 2) if total_candidates else 0

        # Recruiters with at least 1 internship
        recruiters_posted = RecruiterProfile.objects.filter(internships__isnull=False).distinct().count()

        return Response({
            "daily_active_users": daily_active_users,
            "monthly_active_users": monthly_active_users,
            "candidate_profile_completion": completion_rate,
            "recruiters_with_posts": recruiters_posted
        })
class AdminConversionRatesView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        # Profile completion
        users = User.objects.all()
        total_candidates = users.filter(role="candidate").count()
        completed_profiles = CandidateProfile.objects.exclude(resume='').filter(skills__isnull=False).count()
        profile_completion = round((completed_profiles / total_candidates) * 100, 2) if total_candidates else 0

        # Posting → Applications
        total_internships = Internship.objects.count()
        internships_with_apps = Internship.objects.filter(applications__isnull=False).distinct().count()
        post_to_app_conversion = round((internships_with_apps / total_internships) * 100, 2) if total_internships else 0

        # Avg time from recruiter signup to first post
        recruiters = RecruiterProfile.objects.all()
        time_deltas = []
        for rec in recruiters:
            first_post = Internship.objects.filter(recruiter=rec).order_by("created_at").first()
            if first_post:
                delta = (first_post.created_at - rec.created_at).days
                time_deltas.append(delta)

        avg_days = round(sum(time_deltas) / len(time_deltas), 2) if time_deltas else 0

        return Response({
            "signup_to_profile_completion": profile_completion,
            "post_to_app_conversion": post_to_app_conversion,
            "avg_days_to_first_post": avg_days
        })
class AdminTopUsersView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        top_candidates = (
            CandidateProfile.objects
            .annotate(app_count=Count("applications"))
            .order_by("-app_count")[:10]
        )

        top_recruiters = (
            RecruiterProfile.objects
            .annotate(
                post_count=Count("internships"),
                total_apps=Count("internships__applications"),
                shortlisted=Count("internships__applications", filter=Q(internships__applications__shortlisted=True))
            )
            .order_by("-total_apps")[:10]
        )

        return Response({
            "top_candidates": [
                {
                    "full_name": f"{c.first_name} {c.last_name}",
                    "applications": c.app_count
                }
                for c in top_candidates
            ],
            "top_recruiters": [
                {
                    "full_name": f"{r.first_name} {r.last_name}",
                    "internships": r.post_count,
                    "total_applications": r.total_apps,
                    "shortlisted": r.shortlisted,
                    "shortlist_rate": round((r.shortlisted / r.total_apps) * 100, 2) if r.total_apps else 0
                }
                for r in top_recruiters
            ]
        })

# adminpanel/views.py

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from .serializers import FullUserSerializer

class FullUserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FullUserSerializer
    queryset = User.objects.all().order_by('-created_at')
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from adminpanel.permissions import IsAdminRole


class AdminChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def patch(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required."}, status=400)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=400)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "✅ Password changed successfully."}, status=200)
