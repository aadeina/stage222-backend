from django.urls import path
from .views import (
    # 📊 Analytics Views
    PlatformStatsView,
    DailyGrowthSummaryView,
    TopInternshipsView,
    TopRecruitersView,
    TopSkillsView,
    ShortlistRateView,
    AdminGrowthTrendsView,
    AdminEngagementMetricsView,
    AdminConversionRatesView,
    AdminTopUsersView,


    # 👥 User Management Views
    AdminUserListView,
    AdminToggleVerifyUserView,
    AdminToggleActiveUserView,
    AdminDeleteUserView,
    AdminChangeUserRoleView,

    # 📝 Internship Approval Views
    AdminPendingInternshipsView,
    AdminApproveInternshipView,
    AdminRejectInternshipView,
    AdminToggleVerifyOrganizationView
)

urlpatterns = [
    # 📊 Analytics Endpoints
    path('stats/', PlatformStatsView.as_view(), name='admin-platform-stats'),
    path('activity/summary/', DailyGrowthSummaryView.as_view(), name='admin-activity-summary'),
    path('top-internships/', TopInternshipsView.as_view(), name='admin-top-internships'),
    path('top-recruiters/', TopRecruitersView.as_view(), name='admin-top-recruiters'),
    path('top-skills/', TopSkillsView.as_view(), name='admin-top-skills'),
    path('shortlist-rate/', ShortlistRateView.as_view(), name='admin-shortlist-rate'),

    # 👥 User Management Endpoints
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<uuid:id>/verify/', AdminToggleVerifyUserView.as_view(), name='admin-toggle-verify'),
    path('users/<uuid:id>/deactivate/', AdminToggleActiveUserView.as_view(), name='admin-toggle-active'),
    path('users/<uuid:id>/delete/', AdminDeleteUserView.as_view(), name='admin-delete-user'),
    path('users/<uuid:id>/role/', AdminChangeUserRoleView.as_view(), name='admin-change-role'),

    # 📝 Internship Approval Workflow
    path('internships/pending/', AdminPendingInternshipsView.as_view(), name='admin-pending-internships'),
    path('internships/<uuid:id>/approve/', AdminApproveInternshipView.as_view(), name='admin-approve-internship'),
    path('internships/<uuid:id>/reject/', AdminRejectInternshipView.as_view(), name='admin-reject-internship'),
    path('organizations/<uuid:id>/toggle-verify/', AdminToggleVerifyOrganizationView.as_view(), name='admin-toggle-verify-organization'),

    path('analytics/growth/', AdminGrowthTrendsView.as_view()),
    path('analytics/engagement/', AdminEngagementMetricsView.as_view()),
    path('analytics/conversions/', AdminConversionRatesView.as_view()),
    path('analytics/top-users/', AdminTopUsersView.as_view()),


]
