from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .models import ReviewModel
from .forms import SubmitReviewForm

class SubmitReviewView(
    LoginRequiredMixin,
    CreateView,
):
    http_method_names = ['post']
    model = ReviewModel
    form_class = SubmitReviewForm
    
    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data['product']
        messages.success(self.request, 'دیدگاه شما با موفقیت ارسال شد و در صورت تایید منتشر خواهد شد.')
        return redirect(reverse_lazy('shop:product-detail', kwargs={'slug': product.slug}))
    
    def form_invalid(self, form):
        product = form.cleaned_data['product']
        for errors in form.errors.values():
            for error in errors:
                messages.error(self.request, error)
        return redirect(reverse_lazy('shop:product-detail', kwargs={'slug': product.slug}))
    
    

