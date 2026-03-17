from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContactForm, NewsLetterForm

class IndexView(TemplateView):
    template_name = 'website/index.html'

class AboutView(TemplateView):
    template_name = 'website/about.html'

class ContactView(TemplateView):
    template_name = 'website/contact.html'

class SendContactFormView(View):
    http_method_names = ['post']
    form_class = ContactForm
    success_url = reverse_lazy("website:contact")

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تیکت شما ثبت شد.")
            return redirect("website:contact")
        else:
            messages.error(request, "فرم به درستی پر نشده است.دوباره تلاش کنید.")
            return redirect("website:contact")
        
class NewsLetterView(View):
    http_method_names = ['post']
    form_class = NewsLetterForm
    success_url = reverse_lazy("website:index")

    def post(self, request, *args, **kwargs):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت نام شما با موفقیت انجام شد.")
            return redirect("website:index")
        else:
            messages.error(request, "مشکلی به وجود آمد.لطفا دوباره تلاش کنید!")
            return redirect("website:index")