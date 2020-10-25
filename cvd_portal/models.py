from django.db import models
from django.contrib.auth.models import User
import datetime
from dateutil import tz


class CustomDateTimeField(models.DateTimeField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        to_zone = tz.gettz('Asia/Kolkata')
        return value.astimezone(to_zone)


class Device(models.Model):
    user_type = models.CharField(max_length=254, default="", blank=True)
    device_id = models.TextField()

    def __str__(self):
        return self.device_id


class Doctor(models.Model):
    name = models.CharField(max_length=254, default="Somesh")
    hospital = models.CharField(max_length=254, blank=True)
    email = models.EmailField()
    mobile = models.BigIntegerField(blank=True)
    speciality = models.CharField(max_length=102, blank=True)
    designation = models.CharField(max_length=103, blank=True)
    device = models.OneToOneField(Device, null=True, related_name='doctor')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=254, default="Somesh")
    date_of_birth = models.IntegerField(blank=True)
    gender = models.IntegerField(default=1)
    email = models.EmailField(blank=True)
    address = models.TextField(null=True)
    doctor = models.ForeignKey(Doctor, related_name="patients", null=True)
    mobile = models.BigIntegerField(blank=True)
    device = models.OneToOneField(Device, null=True, related_name='patient')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    byte = models.TextField()
    patient = models.ForeignKey(Patient, related_name='image')
    time_stamp = CustomDateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.patient.name + ' ' + str(self.time_stamp)

class PatientData(models.Model):
    patient = models.ForeignKey(Patient, related_name='data')
    systolic = models.IntegerField()
    diastolic = models.IntegerField(default=0)
    weight = models.IntegerField()
    heart_rate = models.IntegerField()
    time_stamp = CustomDateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.patient.name + ' ' + str(self.time_stamp)

class PatientData2(models.Model):
    patient = models.ForeignKey(Patient, related_name='data2')
    time_stamp = CustomDateTimeField(default=datetime.datetime.now)
    ques1_a = models.IntegerField(default=0)
    ques1_b = models.IntegerField(default=0)
    ques1_c = models.IntegerField(default=0)
    ques1_d = models.IntegerField(default=0)
    ques1_e= models.IntegerField(default=0)
    ques1_f= models.IntegerField(default=0)
    ques2 = models.IntegerField(default=0)
    ques3 = models.IntegerField(default=0)
    ques4 = models.IntegerField(default=0)
    ques5 = models.IntegerField(default=0)
    ques6 = models.IntegerField(default=0)
    ques7 = models.IntegerField(default=0)
    ques8 = models.IntegerField(default=0)
    ques9 = models.IntegerField(default=0)
    ques10 = models.IntegerField(default=0)
    ques11 = models.IntegerField(default=0)
    ques12 = models.IntegerField(default=0)
    ques13 = models.IntegerField(default=0)
    ques14 = models.IntegerField(default=0)
    ques15_a = models.IntegerField(default=0)
    ques15_b = models.IntegerField(default=0)
    ques15_c = models.IntegerField(default=0)
    ques15_d = models.IntegerField(default=0)

 
    def __str__(self):
        return self.patient.name + ' ' + str(self.time_stamp)


class OTP(models.Model):
    otp = models.IntegerField()
    user_type = models.TextField()
    user_type_id = models.IntegerField()
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return self.user_type + ' ' + str(self.user_id)


class Notifications(models.Model):
    text = models.TextField()
    patient = models.ForeignKey(
        Patient, null=True, blank=True)
    doctor = models.ForeignKey(
        Doctor, null=True, blank=True)
    time_stamp = CustomDateTimeField(default=datetime.datetime.now)
    isNOTBot = models.BooleanField(default=False, blank=True)

    def __str__(self):
        if(self.patient is None):
            return self.doctor.name + " : " + self.text
        else:
            return self.patient.name + " : " + self.text

class Medicine(models.Model):
    text = models.TextField()
    patient = models.ForeignKey(
        Patient, null=True, blank=True)
    doctor = models.ForeignKey(
        Doctor, null=True, blank=True)
    time_stamp = CustomDateTimeField(default=datetime.datetime.now)

    def __str__(self):
        if(self.patient is None):
            return self.doctor.name + " : " + self.text
        else:
            return self.patient.name + " : " + self.text


class Reminder(models.Model):
    text = models.TextField()
    patient = models.ForeignKey(Patient, null=True, blank=True)
    time = CustomDateTimeField(default=datetime.datetime.now)
    repeat = models.BooleanField(default =True)
    frequency = models.FloatField(default=1.0)
    
    def __str__(self):
        return self.text
