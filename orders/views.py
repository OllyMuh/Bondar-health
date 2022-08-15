from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from .models import OrderItem, Order, Product
from .forms import OrderCreateForm
from cart.views import get_cart, cart_clear

from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint


def order_create(request):
    cart = get_cart(request)
    items = cart.values()
    cart_total_price = sum(Decimal(dic['price']) * dic['quantity'] for dic in items)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            cf = order_form.cleaned_data
            order = order_form.save(commit=False)
            order.save()

            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                cart_item = cart[str(product.id)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )
            cart_clear(request)

            subject = 'Заказ № ' + str(order.id)                # выбирает № из модели OrderItem? - не могу посмотреть чего там внутри - но работает)))
            body = {
                    'first_name': order_form.cleaned_data['first_name'],
                    'last_name': order_form.cleaned_data['last_name'],
                    'email': order_form.cleaned_data['email'],
                    'telephone': order_form.cleaned_data['telephone'],
                    'address': order_form.cleaned_data['address'],
                    'postal_code': order_form.cleaned_data['postal_code'],
                    'city': order_form.cleaned_data['city'],
                    'country': order_form.cleaned_data['country'],
                    'note': order_form.cleaned_data['note'],
                    # 'order': 'Заказ №' + str(order.id)
                }
            message = "\n".join(body.values())

            # generate pdf
            html = render_to_string('pdf.html', {'order': order})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(out)

            # attach file
            # сюда нужно добавить адрес, на который будут приходить сообщения вместо 'sajah@mail.ru'
            email = EmailMessage(subject, message, 'fitness_servis@mail.ru', ['bondarevafitnessdoctor@mail.ru'])
            email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

            try:
                email.send()
            except BadHeaderError:
                return HttpResponse('Неверно заполнены поля формы')
                # return redirect('orders:create')
        return render(request, 'order_created.html', {'order': order})
    else:
        order_form = OrderCreateForm()

    return render(request, 'order_create.html',
                  {'cart': cart,
                   'order_form': order_form,
                   'cart_total_price': cart_total_price,
                   })


# @staff_member_required
def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'

    #generate pdf
    html = render_to_string('pdf.html', {'order': order})
    weasyprint.HTML(string=html).write_pdf(response)
    return response
