from flowershop.flowershopapp.models import User, Bouquet, Category, Order


def get_categories_list():
    return list(Category.objects.all())


def is_user_exist(tg_user_id):
    if User.objects.filter(tg_user_id=tg_user_id).exists():
        user = User.objects.get(tg_user_id=tg_user_id).order_by('-price')
        return user.tg_user_id, user.phone_number, user.name


def add_user(tg_user_id, phone_number, name):
    User.objects.create(tg_user_id=tg_user_id, name=name, phone_number=phone_number)


def get_bouquets_by_filter(category, price):
    bouquets = Bouquet.objects.filter(categories__name=category).filter(price__lte=price)
    return bouquets
