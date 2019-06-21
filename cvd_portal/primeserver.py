from cvd_portal.models import Patient, PatientData, Notifications
from cvd_portal.fcm import send_message

# this function will send the notification to the patient and the doctor related to their uploaded query by the patient
#
# It will work like this:
# query will be recieved by the old django server and it will send to the prime server where all computation will be
# performed in a queue
# and when the job get completed the reponse will send as post request to the old dhadkan server and by parsing notificaation will be send

def notification_save(data):
    p = Patient.objects.get(pk=pk)
    d_id = p.doctor.device.device_id
    p_id = p.device.device_id
    send_message(d_id, None, doc_message)
    send_message(p_id, None, patient_message)
    Notifications(text=doc_message, doctor=p.doctor).save()
    Notifications(text=patient_message, patient=p).save()


def call_server(data):

    # API call to the Server

    return


def recieve_server(data):

    # get data from the server and trigger notofication

    return
