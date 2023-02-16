from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE, FloatField, AutoField, ManyToManyField


# ----------------------------------------------------------------
# Location model
class Location(Model):
    name = CharField(max_length=50)
    lat = FloatField()
    lng = FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


# ----------------------------------------------------------------
# User model
class User(Model):
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=50)
    username = CharField(max_length=50)
    password = CharField(max_length=50)
    role = CharField(max_length=50)
    age = IntegerField()
    locations = ManyToManyField('users.Location')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
