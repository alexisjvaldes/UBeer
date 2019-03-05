from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    role = models.IntegerField(max_length=2)
class Establishments(models.Model):
    user_ID = models.ForeignKey(Users, on_delete=models.CASCADE)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    address = models.CharField(max_length=100)
    zipCode = models.IntegerField(max_length=5)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=2)
class Menu(models.Model):
    establishment_ID = models.ForeignKey(Establishments, on_delete=models.CASCADE)
    name = models.CharField()
    price = models.FloatField()
class Transactions(models.Model):
    user_ID = models.ForeignKey(Users, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateTimeField()
    establishment_ID = models.ForeignKey(Establishments, on_delete=models.CASCADE)
class TransactionsMenu(models.Model):
    transactionID = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    menuID = models.ForeignKey(Menu, on_delete=models.CASCADE)