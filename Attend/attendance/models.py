from django.db import models
from django.utils import timezone
from datetime import datetime,date
# Create your models here.
class Atten(models.Model):
    Name = models.CharField(max_length=120)
    Empid = models.AutoField(primary_key=True)
    Dept = models.CharField(max_length=150)
    Joining = models.DateTimeField(default=timezone.now)
    Date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table='atten'
class Attenwork(models.Model):

    date = models.DateField(default=datetime.now)
    Empid = models.ForeignKey(Atten, on_delete=models.CASCADE,primary_key=True)
    timein = models.TimeField(null=True)
    # temps_preperation = models.DateTimeField(null=True)
    lunchin = models.TimeField(null=True)
    lunchout = models.TimeField(null=True)
    breakin = models.TimeField(null=True)
    breakout = models.TimeField(null=True)
    logout = models.TimeField(null=True)
    totalhour = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
     
    class Meta:
        db_table='enterattendance'

