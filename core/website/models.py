from django.db import models

class ContactModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=12, blank=True, null=True
    )
    subject = models.CharField(
        max_length=255, blank=True, null=True
    )
    message = models.TextField(max_length=700)
    is_checked = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class NewsLetter(models.Model):
    email = models.EmailField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email