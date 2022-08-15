from django.urls import path
from pages.views import homepage, about_us, contact, photo_filter

app_name = 'pages'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('about_us/', about_us, name='about_us'),
    path('photo_filter/<int:category_photo_pk>/', photo_filter, name='photo_filter'),
    path('contact/', contact, name='contact'),
]