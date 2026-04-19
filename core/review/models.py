from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.db.models import Avg
from django.dispatch import receiver

from shop.models import Product

class ReviewStatusType(models.IntegerChoices):
    pending = 1, 'در حال بررسی'
    accepted = 2, 'تایید شده'
    rejected = 3, 'رد شده'

class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(
        default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatusType.choices,
        default=ReviewStatusType.pending.value)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]


    def __str__(self):
        return self.user.email

    def get_status(self):
        return {
            "id": self.status,
            "title": ReviewStatusType(self.status).name,
            "label": ReviewStatusType(self.status).label,
        }
    
@receiver(post_save, sender=ReviewModel)
def avg_rate_calculate(sender, instance, *args, **kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        average_rating = ReviewModel.objects.filter(
            product=instance.product,
            status=ReviewStatusType.accepted
        ).aggregate(Avg('rate'))['rate__avg']
        Product.objects.filter(pk=instance.product.pk).update(avg_rate=round(average_rating, 1))
        