from cvd_portal.models import Notifications
import csv

#
# with open('Notifications.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile)
#     # write your header first
#     for obj in Notifications.objects.all():
#         row = ""
#         for field in fields:
#              row += getattr(obj, field.name) + ","
#         writer.writerow(row)



with open('Notifications.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    # write your header first
    for obj in Notifications.objects.all():
        row = [obj.doctor,obj.patient,obj.text]
        writer.writerow(row)
