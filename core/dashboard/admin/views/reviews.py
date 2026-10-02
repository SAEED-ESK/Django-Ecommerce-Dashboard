from django.views.generic import (
    ListView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from ..forms.reviews import AdminReviewEditForm
from review.models import ReviewModel, ReviewStatusType
from ...permissions import AdminHasAccessPermission

class AdminReviewListView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    ListView
    ):
    template_name = 'dashboard/admin/reviews/review-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = ReviewModel.objects.all()
        order_by = self.request.GET.get('order_by')
        status = self.request.GET.get('status')
        search_q = self.request.GET.get('q')
        if status:
            queryset = queryset.filter(status=status)
        if search_q:
            queryset = queryset.filter(product__title__icontains=search_q)
        if order_by:
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['status_types'] = ReviewStatusType.choices
        return context
    
class AdminReviewEditView(
    LoginRequiredMixin,
    AdminHasAccessPermission,
    SuccessMessageMixin,
    UpdateView
    ):
    template_name = 'dashboard/admin/reviews/review-edit.html'
    queryset = ReviewModel.objects.all()
    form_class = AdminReviewEditForm
    success_message = 'تغییرات با موفقیت ثبت شد.'

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:review-edit', kwargs={'pk': self.kwargs.get('pk')})