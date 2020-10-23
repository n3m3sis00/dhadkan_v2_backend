from django.core.mail import send_mail

from cvd_portal.models import Patient, PatientData, Notifications
from cvd_portal.fcm_d import send_message
import datetime
import os
from .ocr import ocr_space_file_

import difflib
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


def gen_abcd_message(medicines):
    response_data = []
    user_data = {
        "extra_med" : [],
        'a':[],
        'b':[],
        'c':[],
        'd':[]
    }
    medicine_ = {
        
	"apixaban" : "a" ,
	"dabigatran" : "a",
	"edoxaban" : "a",
	"heparin" : "a",
	"rivaroxaban" : "a",
	"warfarin" : "a",
	"aspirin" : "a",
	"clopidogrel" : "a",
	"dipyridamole" : "a",
	"prasugrel" : "a",
	"ticagrelor" : "a",
	"benazepril" : "a",
	"captopril" : "a",
	"enalapril" : "a",
	"fosinopril" : "a",
	"lisinopril" : "a",
	"moexipril" : "a",
	"perindopril" : "a",
	"quinapril" : "a",
	"ramipril" : "a",
	"trandolapril" : "a", 
	"azilsartan" : "a",
	"candesartan" : "a",
	"eprosartan" : "a",
	"irbesartan" : "a",
	"losartan" : "a",
	"olmesartan" : "a", 
	"telmisartan" : "a", 
	"valsartan" : "a", 
	"sacubitril" : "a",
	"acebutolol" : "b",
	"atenolol" : "b",
	"betaxolol" : "b",
	"hydrochlorothiazide" : "b",
	"bisoprolol" : "b",
	"metoprolol" : "b",
	"nadolol" : "b",
	"propranolol" : "b",
	"sotalol" : "b",
	"carvedilol" : "b",
	"labetalol hydrochloride" : "b",
	"amlodipine" : "c",
	"diltiazem" : "c",
	"felodipine" : "c",
	"nifedipine"  : "c",
	"nimodipine" : "c",
	"nisoldipine" : "c",
	"verapamil" : "c",
	"atorvastatin" : "c",
	"fluvastatin" : "c", 
	"lovastatin" : "c", 
	"pitavastatin" : "c", 
	"pravastatin" : "c",
	"rosuvastatin" : "c", 
	"simvastatin" : "c",
	"niacin" : "c",
	"ezetimibe" : "c", 
	"ezetimibe" : "c",
	"simvastatin" : "c", 
	"digoxin" : "d",
	"acetazolamide" : "d",
	"amiloride" : "d",
	"bumetanide" : "d",
	"chlorothiazide" : "d",
	"chlorthalidone" : "d",
	"furosemide" : "d",
	"hydro chlorothiazide" : "d",
	"indapamide" : "d", 
	"metalozone" : "d",
	"spironolactone" : "d",
	"torsemide" : "d"
    }
    for medicine in medicines:
        if list(medicine_.keys()).count(medicine) == 0:
            user_data['extra_med'].append(medicine)

        else:
            user_data[medicine_[medicine]].append(medicine)

    for key,value in user_data.items():
        if len(value) == 0:
            if key == "extra_med":
                continue
            response_data.append("Type "+ key + " medicine missing")
        elif key == "extra_med":
            response_data.append("Extra Medicines given: " + str(value))
        else:
            response_data.append("")


    strins_response = "\n".join([ x for x in response_data])

    return strins_response

def get_parsed_ocr_results(data):
    
    message = ""
    
    with open('/app/cvd_portal/medicine.txt', 'r') as med_file:
        medicines = med_file.readlines()
        found_med_name = []
        found_med_name_prob = []
        database_med = []
        for i in medicines:
            close_match = difflib.get_close_matches(i.replace("\n", ""), data)
            
            if len(close_match) != 0:
                database_med.append(i)
                found_med_name.append(close_match[0])
            else:
                continue

      
        if len(found_med_name) != 0:
            print("hi from true")
            print(found_med_name)
            print(database_med)
            
            found_med_name = list(set(found_med_name))
            data_base_med = [x.replace("\n","") for x in database_med]
            
            print(data_base_med, found_med_name)
            extracted_name = ", ".join(found_med_name)
            expected_name = ", ".join(data_base_med)
            
            print(expected_name)

            message = "Extracted Name: " + extracted_name + "\nExpected Name: " + expected_name  

            print(message)       

            return True, message
        else:
            print("hi from false")
            return False, "No Medicinal Information Found in submitted Image for OCR"
        
def send_ocr_notification(mobile):
    print("hi from ocr notification")
    p = Patient.objects.get(mobile= int(mobile))

    p_id = p.device.device_id
    d_id = p.doctor.device.device_id
    
    data_ocr = ocr_space_file_()
    data_ocr_ = [x.lower() for x in data_ocr]
    print(data_ocr)
    ismessage, message = get_parsed_ocr_results(data_ocr_)
    print(ismessage, message)    
    print(p.name)
    patient_noti = message + "\n\n" + "-------------------\n" + "\n".join(data_ocr_)
    doc_message = p.name + " has submitted an OCR Request\n\n" + patient_noti

    if ismessage:
        send_message(d_id, None, doc_message)
        # send_message(p_id, None, patient_noti)

        Notifications(text=doc_message, doctor=p.doctor).save()
        Notifications(text=patient_noti, patient=p).save()
    else:
        Notifications(text=doc_message, doctor=p.doctor).save()
        Notifications(text=patient_noti, patient=p).save()

        send_message(d_id, None, doc_message)
        # send_message(p_id, None, patient_noti)

    return patient_noti

def send_abcd_notification(data,mobile):
    timestamp_to = datetime.datetime.now() - datetime.timedelta(days=8)
    print(mobile)
    print(type(mobile))
    p = Patient.objects.get(mobile=int(mobile))

    print("------------------")
    print(p)
    print(p.name)
    print(p.doctor)
    print("-----------------")
    response_ = ""
    if data != []:
        response_ = gen_abcd_message(data)
        print(response_)

    if(len(response_) == 0):
        return
    else:
        d_id = p.doctor.device.device_id
        p_id = p.device.device_id
        send_message(d_id, None, response_)
        patient_message = response_ 
        print(patient_message)
        send_message(p_id, None, patient_message)
        Notifications(text=patient_message, doctor=p.doctor).save()
        Notifications(text=patient_message, patient=p).save()


## Support Email
def send_email_support(msg, user):
    print("Sending MSG")
    message = user.name + "\n\n" + msg
    print(message)
    send_mail('Dhadkan Report', message, 'noreply@dhadkan.co', ['shreya2feb@gmail.com', 'durgesh123.iitr@gmail.com'], fail_silently=False)
    return 