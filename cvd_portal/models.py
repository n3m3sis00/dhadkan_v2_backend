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
    user_type = models.CharField(max_length=20, default="", blank=True)
    device_id = models.TextField()

    def __str__(self):
        return self.device_id


class Doctor(models.Model):
    name = models.CharField(max_length=60, default="Somesh")
    hospital = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    mobile = models.BigIntegerField(blank=True)
    speciality = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    device = models.OneToOneField(Device, null=True, related_name='doctor')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=60, default="Somesh")
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
    ques1_a = models.IntegerField()
    ques1_b = models.IntegerField()
    ques1_c = models.IntegerField()
    ques1_d = models.IntegerField()
    ques1_e= models.IntegerField()
    ques1_f= models.IntegerField()
    ques2 = models.IntegerField()
    ques3 = models.IntegerField()
    ques4 = models.IntegerField()
    ques5 = models.IntegerField()
    ques6 = models.IntegerField()
    ques7 = models.IntegerField()
    ques8 = models.IntegerField()
    ques9 = models.IntegerField()
    ques10 = models.IntegerField()
    ques11 = models.IntegerField()
    ques12 = models.IntegerField()
    ques13 = models.IntegerField()
    ques14 = models.IntegerField()
    ques15_a = models.IntegerField()
    ques15_b = models.IntegerField()
    ques15_c = models.IntegerField()
    ques15_d = models.IntegerField()

 
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
