from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.postgres.fields import JSONField

from plans.models import Plan, Doctors
from users.models import Patient



class PatientPlan(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='packages')
    package = models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='patients')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    transaction_id = models.CharField(max_length=20)



class AvailableSlots(models.Model):
    start_time  = models.DateTimeField()
    end_time = models.DateTimeField()


class DoctorConfirmedSlots(models.Model):
    doctor = models.ForeignKey(Doctors,on_delete=models.CASCADE,related_name='confirmed_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()



class SessionBooking(models.Model):
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='sessions')
    session = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time= models.DateTimeField(null=True,blank=True)
    video_conferencing_link= models.CharField(max_length=300)
    is_attended = models.BooleanField(default=False)
    remarks = models.CharField(max_length=400)
    date_of_booking = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctors,related_name='booked_sessions',on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='sessions')


class SessionWiseHealthRecord(models.Model):
    session = models.ForeignKey(SessionBooking,on_delete=models.CASCADE,related_name='healthrecords')
    attrs = JSONField() # Answers corresponding to every question .
    date_submitted = models.DateTimeField(blank=True,null=True)


#     # Create a Profile with preferences
# p = Profile(name="Tanner", preferences={'sms': False, 'daily_email': True, 'weekly_email': True})
# p.save()

# results = Profile.objects.filter(preferences__daily_email=True)
# If you want to check the SQL query that Django runs, you can print it from the query property on the results object:
#
# print(results.query)
# # Output:
# SELECT "app_profile"."id", "app_profile"."name", "app_profile"."preferences"
# FROM "app_profile" WHERE ("app_profile"."preferences" -> daily_email) = 'true'


# results = Profile.objects.filter(preferences__sms__isnull=True)




