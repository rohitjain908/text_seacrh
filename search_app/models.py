from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    brand = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    subCategory = models.CharField(max_length = 100)


    def __str__(self):
        return self.name



class DictKey(models.Model):
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)


    def __str__(self):
        return self.name


class DictKeyValue(models.Model):
    container = models.ForeignKey(DictKey, on_delete = models.CASCADE)
    key = models.CharField(max_length = 100)
    value = models.CharField(max_length = 100)


    def __str__(self):
        return self.value


    
