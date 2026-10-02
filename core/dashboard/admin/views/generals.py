from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import AdminHasAccessPermission


class AdminHomeView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    TemplateView
    ):
    template_name = 'dashboard/admin/home.html'