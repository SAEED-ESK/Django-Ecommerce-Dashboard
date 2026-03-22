from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductStatusType(models.IntegerChoices):
    publish = 1, ("نمایش")
    draft = 2, ("عدم نمایش")

class ProductCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategory)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(
        default='/default/product-img.png', upload_to='product/img/'
    )
    description = models.TextField()
    brief_description = models.TextField(blank=True, null=True)
    status = models.IntegerField(
        choices=ProductStatusType.choices,
        default=ProductStatusType.draft.value
    )
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=0
    )
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def get_price(self):
        show_price = self.price - (self.price * self.discount_percent / 100)
        return round(show_price)
    
    def get_show_price(self):
        show_price = self.price - (self.price * self.discount_percent / 100)
        return '{:,}'.format(round(show_price))

    def get_show_raw_price(self):
        return '{:,}'.format(self.price)
    
    def is_discounted(self):
        return self.discount_percent != 0

    def __str__(self):
        return self.title

class ProductImageModel(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product/extra-img/')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)