from django.db import models

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
    status = models.IntegerField(
        choices=ProductStatusType.choices,
        default=ProductStatusType.draft.value
    )
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=0
    )
    discount_percent = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

class ProductImageModel(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product/extra-img/')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)