from django.db import models
from django.core.management import sql, color

# Create your models here.
class QR(models.Model):
  qrid = models.CharField(max_length=10)
  qtype = models.CharField(max_length=50)
  status = models.CharField(max_length=50)

class types(models.Model):
  typeid = models.IntegerField()
  qtype = models.CharField(max_length=50, primary_key=True)