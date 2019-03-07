from django.db import models


class Users(models.Model):
    ROLE_CHOICES = (
        ('R', 'Rider'),
        ('E', 'Establishment')
    )

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    role = models.CharField(choices=ROLE_CHOICES, max_length=1)


class Establishments(models.Model):
    user = models.ForeignKey(Users, on_delete=None)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    address = models.CharField(max_length=128)
    zipCode = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        try:
            int(self.zipCode)
        except ValueError:
            raise Exception("Invalid Zip Code")

        super(Establishments).save(self, *args, *kwargs)

    
class Menu(models.Model):
    establishment = models.ForeignKey(Establishments, on_delete=None)
    name = models.CharField(max_length=128)
    price = models.FloatField()


class Transactions(models.Model):
    user = models.ForeignKey(Users, on_delete=None)
    total = models.FloatField()
    date = models.DateTimeField()
    establishment = models.ForeignKey(Establishments, on_delete=None)


class TransactionsMenu(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=None)
    menuID = models.ForeignKey(Menu, on_delete=None)
