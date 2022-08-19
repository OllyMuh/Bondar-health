from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError

from pages.forms import ContactForm
from pages.models import CategoryPhoto, Photo

# import logging
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d %I:%M:%S %p', handlers=[logging.handlers.SMTPHandler('smtp.mail.ru', 'fitness_servis@mail.ru', ['fitness_servis@mail.ru'], 'LYYDownloader Server Exception', credentials=('fitness_servis@mail.ru', 'SJhcmYV7REwyCmsazJgx'))])

def homepage(request):
    return render(request, 'index.html')


def about_us(request):
    # breakpoint()
    categories = CategoryPhoto.objects.all()
    photos = Photo.objects.all()
    context = {
        'categories': categories,
        'photos': photos,
    }
    return render(request, 'about-us.html', context)


def photo_filter(request, category_photo_pk):
    categories = CategoryPhoto.objects.all()
    photos = Photo.objects.all().filter(category_photo__pk=category_photo_pk)
    context = {
        'categories': categories,
        'photos': photos,
    }
    return render(request, 'about-us.html', context)


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            body = {
                'sender': contact_form.cleaned_data['sender'],
                'email': contact_form.cleaned_data['email'],
                'message': contact_form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                # сюда нужно добавить адрес, на который будут приходить сообщения вместо 'sajah@mail.ru'
                send_mail(subject, message, 'fitness_servis@mail.ru', ['bondarevafitnessdoctor@mail.ru'])
            except BadHeaderError:
                return HttpResponse('Неверно заполнены поля формы')
            return redirect('pages:contact')

    contact_form = ContactForm()
    return render(request, 'contact.html', {'contact_form': contact_form})