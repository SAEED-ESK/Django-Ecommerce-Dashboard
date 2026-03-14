from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import Product, ProductStatusType

class ProductGridView(ListView):
    template_name = 'shop/product_grid.html'
    queryset = Product.objects.filter(
        status=ProductStatusType.publish.value
    )
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context

class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    queryset = Product.objects.filter(
        status=ProductStatusType.publish.value
    )