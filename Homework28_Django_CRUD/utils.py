import csv

from Homework28_Django_CRUD.settings import ADS_PATH, CAT_PATH, LOC_PATH, US_PATH
from ads.models import Category, Advertisement
from users.models import User, Location


# ----------------------------------------------------------------
def convert_csv(file) -> list[dict]:
    """
    Convert a CSV file to list with dict
    :param file: CSV file
    :return: list of dict
    """
    with open(file, encoding='utf-8') as f:
        return [row for row in csv.DictReader(f)]


# ----------------------------------------------------------------
def fill_database() -> None:
    """
    Fill the database with data from CSV files
    :return: None
    """
    categories: list[dict] = convert_csv(file=CAT_PATH)
    ads: list[dict] = convert_csv(file=ADS_PATH)
    locations: list[dict] = convert_csv(file=LOC_PATH)
    users: list[dict] = convert_csv(file=US_PATH)
    for category_ in categories:
        category = Category.objects.create(**category_)
        category.save()
    for location_ in locations:
        location = Location.objects.create(**location_)
        location.save()
    for user_ in users:
        user = User.objects.create(**user_)
        user.save()
    for ad_ in ads:
        if ad_['is_published'] == 'TRUE' or ad_['is_published'] == 'FALSE':
            ad_['is_published'] = ad_['is_published'].title()
        ad = Advertisement.objects.create(**ad_)
        ad.save()


