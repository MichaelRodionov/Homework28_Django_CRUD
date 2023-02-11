from django.db.models import Model, IntegerField, CharField, \
    BooleanField, ForeignKey, CASCADE, ImageField

from users.models import User


# ----------------------------------------------------------------
# Category model
class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# ----------------------------------------------------------------
# Advertisement model
class Advertisement(Model):
    name = CharField(max_length=400)
    author = ForeignKey(User, on_delete=CASCADE)
    price = IntegerField()
    description = CharField(max_length=1000)
    is_published = BooleanField()
    image = ImageField(upload_to='images/')
    category = ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
