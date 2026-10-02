from django import forms
from .models import ContactModel, NewsLetter

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'subject',
            'message'
        ]

class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = [
            'email'
        ]

    def save(self, commit=True):
        newsLetter, created = NewsLetter.objects.get_or_create(email=self.data.get('email'))
        return newsLetter