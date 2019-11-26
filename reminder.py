import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhadkan.settings")
import django
from datetime import datetime
from datetime import timedelta

django.setup()

from cvd_portal.fcm_d import send_message
from cvd_portal.models import Reminder
from django.utils import timezone
now = timezone.now()

def notify():
    reminders = Reminder.objects.all()
    for rem in reminders:
        if rem.time <= now:
            
            pat = rem.patient
            device_id = pat.device.device_id

            text = rem.text

            
            send_message(device_id,"me",text)
            print("Notification send to :", pat.name, datetime.now())

            repeat = rem.repeat

            if not repeat:
                rem.delete()
            else:
                freq = rem.frequency

                rem.time = rem.time + timedelta(days = int(freq))
                rem.save()



        else:
            continue


if __name__ == "__main__" :
    notify()


print("not main")
