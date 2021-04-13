import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhadkan.settings")
import django
from datetime import datetime
from datetime import timedelta

django.setup()

from cvd_portal.fcm_d import send_message
from cvd_portal.models import PatientData, Patient
from django.utils import timezone
now = timezone.now()

def notify():
    patients = Patient.objects.all()
    for pat in patients:
        try:
            data = PatientData.objects.filter(patient=pat).order_by('-time_stamp')[0]
            if data.time_stamp + timedelta(days=14) <= now:
        
                device_id = pat.device.device_id
                doc_device_id = pat.doctor.device.device_id
    
                text_pat = "You have not sent the data from past 14 days, kindly send new data"
                text_doc = pat.name + " has not sent data in past 2 weeks"
    
                
                send_message(device_id,"me",text_pat)
                send_message(doc_device_id,"me", text_doc)
                print("Notification send to :", pat.name, datetime.now())

            else:
                continue
        except:
            continue



if __name__ == "__main__" :
    notify()



