from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import Product, ProductStatusType

class ProductGridView(ListView):
    template_name = 'shop/product_grid.html'
    queryset = Product.objects.filter(status=ProductStatusType.publish.value)
