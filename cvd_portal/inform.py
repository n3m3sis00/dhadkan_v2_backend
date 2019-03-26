from cvd_portal.models import Patient, PatientData, Notifications
from cvd_portal.fcm import send_message
import datetime

#change_observed = [False, False, False, False]


def gen_message(co, p):
    gen_msg = False
    for c in co:
        if c is True:
            gen_msg = True
    if gen_msg is False:
        return None
    else:
        message = "Patient named '" + p.name + "' suffered drastic changes in "
        if(co[0] is True):
            message = message + "'weight' "
        if(co[1] is True):
            message = message + "'heart-rate' "
        if(co[2] is True):
            message = message + "'BP-systolic' "
        if(co[3] is True):
            message = message + "'BP-diastolic' "
        message = message + "in recent few days."
        return message


def get_patient(pk):
    return Patient.objects.get(pk=pk)


def check(request):
    change_observed = [False, False, False, False]
    timestamp_to = datetime.datetime.now() - datetime.timedelta(days=8)
    p = get_patient(request.data['patient'])
    print('\n All patient data : {}\n {}\n'.format(type(p),p))
    pd = PatientData.objects.filter(
        patient_id=request.data['patient'],
        time_stamp__gte=timestamp_to).order_by('-time_stamp')
    print('\n Filtered patient data :\n {}\n'.format(pd))
    if(len(pd) == 0):
        return
    else:
        print("\n\nIn Else :\n")
        wt = int(request.data['weight'])
        hr = int(request.data['heart_rate'])
        sys = int(request.data['systolic'])
        dia = int(request.data['diastolic'])
        print('weight {} hr {} sys {} dia{}'.format(wt,hr,sys,dia))
        print('request data \n {}'.format(request.data))
        for d in pd:
            print("Printing for loop \n\n")
            if(abs(d.weight-wt) >= 1):
                print('1. weight \n wt {} dwt {} \n'.format(wt,d.weight))
                change_observed[0] = True
            if(abs(abs(d.heart_rate) - hr)/hr >= 0.1):
                print('2. Heart Rate \n hr {} dhr {}  \n'.format(hr,d.heart_rate))
                change_observed[1] = True
            if(abs(abs(d.systolic) - sys)/sys >= 0.1):
                print('3. Systel \n sys {} after_sys {} \n'.format(sys,d.systolic))
                change_observed[2] = True
            if(abs(abs(d.diastolic) - dia)/dia >= 0.1):
                print('4. Diastole \n dys {} after_dys {} \n'.format(dia,d.diastolic))
                change_observed[3] = True
        doc_message = gen_message(change_observed, p)
        print('Change Observerd array at end [weight,heart,sys,dia]: \n\n{}'.format(change_observed))
        if(doc_message is None):
            return
        else:
            d_id = p.doctor.device.device_id
            p_id = p.device.device_id
            send_message(d_id, None, doc_message)
            patient_message = "Please visit nearest OPD"
            send_message(p_id, None, patient_message)
            Notifications(text=doc_message, doctor=p.doctor).save()
            Notifications(text=patient_message, patient=p).save()
