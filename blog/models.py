from django.db import models

from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(
        max_length=48, blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='категория', related_name='posts'
    )
    title = models.CharField(
        max_length=64,
        verbose_name='заголовок',
        blank=True, null=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True, null=True
    )
    text = models.TextField(
        verbose_name='текст'
    )
    image = models.ImageField(
        upload_to='blog',
        verbose_name='картинка',
        blank=True, null=True
    )
    published = models.DateField(
        verbose_name='дата публикации',
        default=timezone.now
    )
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE,
    #     blank=True, null=True
    # )
    # likes = models.IntegerField(
    #     verbose_name='Like',
    #     default=0,
    #     blank=True, null=True
    # )
    # dislikes = models.IntegerField(
    #     verbose_name='Dislike',
    #     default=0,
    #     blank=True, null=True
    # )

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f'{self.title}'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    published_date = models.DateTimeField(
        verbose_name='Дата публикации',
    )
    author = models.CharField(max_length=40, blank=True, null=True, default='', verbose_name='Автор')

    def __str__(self):
        return f'{self.text}'
