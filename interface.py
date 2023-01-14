from flowershopapp.models import User, Bouquet, Category, Order


def get_categories():
    return [category.name for category in Category.objects.all()]


def add_category(category):
    Category.objects.update_or_create(name=category)


def is_user_exist(tg_user_id):
    if User.objects.filter(tg_user_id=tg_user_id).exists():
        user = User.objects.get(tg_user_id=tg_user_id)
        return user.tg_user_id, user.phone_number, user.name


def add_user(tg_user_id, phone_number, name):
    User.objects.create(tg_user_id=tg_user_id, name=name, phone_number=phone_number)


def get_bouquets_by_filter(category, price):
    bouquets = Bouquet.objects.filter(categories__name=category).filter(price__lte=price).order_by('-price')
    return bouquets

if __name__ == '__main__':

    bouquets = Bouquet.objects.filter(categories__name=category).filter(price__lte=price).order_by('-price')
