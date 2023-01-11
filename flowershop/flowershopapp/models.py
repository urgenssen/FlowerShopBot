from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=200,
    )

    def __str__(self):
        return f'{self.name}'


class User(models.Model):
    name = models.CharField(
        'Имя пользователя',
        max_length=200,
        db_index=True,
    )
    phone_number = models.CharField(
        'Номер телефона пользователя (без "+7")',
        max_length=10,
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return f'{self.name} - {self.phone_number}'


class Bouquet(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        null=False,
        blank=False,
    )
    img_url = models.CharField(
        'Ссылка на изображение',
        max_length=200,
        null=False,
        blank=False,
    )
    text = models.TextField(
        'Описание',
        max_length=200,
        null=False,
        blank=False,
    )
    content = models.TextField(
        'Состав',
        max_length=200,
        null=False,
        blank=False,
    )
    price = models.DecimalField(
        'Цена',
        max_digits=6,
        decimal_places=2,
        blank=False,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категория',
#        related_name='bouquets',
        blank=True,
    )

    def __str__(self):
        return f'{self.name} - {self.price}'


class Order(models.Model):
    date_time = models.DateTimeField(
        'Время заказа',
        auto_now=True,
        null=False,
        blank=False,
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Заказчик',
        null=False,
        blank=False,
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        verbose_name='Букет',
        null=False,
        blank=False,
    )
    delivery_date_time = models.DateTimeField(
        'Дата и время доставки',
        null=False,
        blank=False,
    )
    address = models.TextField(
        'Адрес доставки: Город, Улица, Строение, Помещение',
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.date_time} - {self.customer} - {self.delivery_date_time}'
