from flowershopapp.models import User, Bouquet, Category, Order
from django.shortcuts import get_object_or_404


def get_categories():
    return [category.name for category in Category.objects.all()]


def add_category(category):
    Category.objects.update_or_create(name=category)


def get_user(tg_user_id):
    try:
        user = User.objects.get(tg_user_id=tg_user_id)
    except User.DoesNotExist:
        return None

    return user


def add_user(tg_user_id, phone_number, name):
    User.objects.update_or_create(
        tg_user_id=tg_user_id,
        name=name,
        phone_number=phone_number,
    )


def get_bouquets_by_filter(category, price):
    bouquets = Bouquet.objects.filter(categories__name=category).filter(price__lte=price).order_by('-price')
    return bouquets


def get_bouquets(price=100000):
    bouquets = Bouquet.objects.filter(price__lte=price).order_by('-price')
    return bouquets

def create_order(user_data):
    bouquet = Bouquet.objects.get(user_data['bouquet_id']) # ссылка на выбранный букет
    # TODO создать заказ
