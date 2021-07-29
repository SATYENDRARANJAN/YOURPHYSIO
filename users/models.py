from datetime import datetime

from django.db import models

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=40,null=True)
    phone = models.IntegerField(max_length=10)
    email = models.EmailField()
    created_at=models.DateTimeField(default=datetime.now)
    updated_at=models.DateTimeField(default=datetime.now)


class Profile(models.Model):
    patient= models.OneToOneField(Patient,related_name='profile',on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    #other personal data


class HealthQuestions(models.Model):
    QTYPES=(('multiple_choice','multiple_choice'),('text_input','text_input'),('numeric_input','numeric_input'),('upload_file','upload_file'))
    qcode = models.CharField(max_length=10)
    qtext = models.CharField(max_length=100)
    order = models.IntegerField()
    qtype = models.CharField(max_length=40,choices=QTYPES)


class SubQuestions(models.Model):
    question = models.ForeignKey(HealthQuestions,related_name='subquestions',on_delete=models.CASCADE)
    subqtext = models.CharField(max_length=100)
    order= models.IntegerField()

class HealthInfoRecords(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='records')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    session_count = models.IntegerField(default=0)




class PatientGoals(models.Model):
    pass



