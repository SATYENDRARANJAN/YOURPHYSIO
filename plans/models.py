from django.db import models

# Create your models here.
class Doctors(models.Model):
    SPECIALIZATIONS = (('KNEE','knee'),('spine','spine'),('pelvis','pelvis'),('neck_shoulder','neck_shoulder'))
    name = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=50,choices=SPECIALIZATIONS)






class Plan(models.Model):
    plancode =models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=3 , max_digits=7)
    sessions_alloted = models.IntegerField()




