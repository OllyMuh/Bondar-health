from django.db import models


# model to show photos by categories on the page "about us"
class CategoryPhoto(models.Model):
    title = models.CharField(
        max_length=48, blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}'


# model to show photos from the base
class Photo(models.Model):
    image = models.ImageField(
        verbose_name="Фото",
        upload_to='pages',
        default='static/img/yoga-1.jpg'                  # change default!!!
    )
    category_photo = models.ForeignKey(
        CategoryPhoto,
        on_delete=models.CASCADE,
        verbose_name='Тема',
        related_name='photos'
    )
