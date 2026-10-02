from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import CustomerHasAccessPermission


class CustomerHomeView(
    LoginRequiredMixin,
    CustomerHasAccessPermission,
    TemplateView
    ):
    template_name = 'dashboard/customer/home.html'