from django.shortcuts import render, redirect, get_object_or_404

from elements.forms import ReviewForm
from elements.models import Product, Review
from cart.forms import CartAddProductForm


def product_list(request):
    products = Product.objects.all()
    return render(request, 'elements/elements.html',
                  {
                    'products': products,
                    })


def product_detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cf = review_form.cleaned_data
            author_name = "Имя"
            Review.objects.create(product=product, author=author_name, rating=cf['rating'], text=cf['text'])
            return redirect(
                'elements:product_detail', product_pk=product.pk
            )
    else:
        review_form = ReviewForm()
        cart_product_form = CartAddProductForm()
        return render(request, 'elements/element_detail.html', {
            'product': product,
            'review_form': review_form,
            'cart_product_form': cart_product_form
        })