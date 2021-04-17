from django.core.mail import send_mail

from cvd_portal.models import Patient, PatientData, Notifications, Image
from cvd_portal.fcm_d import send_message
import datetime
import os
from .ocr import ocr_space_file_
from .medicines import MEDICINES
from dhadkan.settings import BASE_DIR

import difflib
import base64
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
    medicine_ = MEDICINES
    print(medicine_)
    for medicine in medicines:
        medicine = medicine.replace(" ", "").lower()
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
            response_data.append("--")


    strins_response = "\n".join([ x for x in response_data if x != "--"])

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

            # message = "--------------------------------\nExtracted Name: \n--------------------------------\n" \
            # + extracted_name + "\n--------------------------------\nExpected Name:\n--------------------------------\n" + expected_name  

            message = "Extracted Medicine:\n--------------------------------\n" + expected_name  

            abcd = gen_abcd_message(data_base_med)
            message += "\n--------------------------------------------\n" + abcd
            print(message)       

            return True, message
        else:
            print("hi from false")
            return False, "No Medicinal Information Found in submitted Image for OCR"
        
def send_ocr_notification(mobile, filename_):
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
    patient_noti = message
    doc_message = p.name + " has submitted an OCR Request\n\n" + patient_noti

    import base64

    with open(os.path.join(BASE_DIR, filename_), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    im = Image(byte = encoded_string, patient=p)
    im.save()

    if ismessage:
        send_message(d_id, None, doc_message)
        Notifications(text=doc_message, image = im, doctor=p.doctor).save()
        Notifications(text=patient_noti,  image = im, patient=p).save()
    else:
        Notifications(text=doc_message,  image = im, doctor=p.doctor).save()
        Notifications(text=patient_noti,  image = im, patient=p).save()

        send_message(d_id, None, doc_message)
        # send_message(p_id, None, patient_noti)

    return patient_noti, im.id

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

def checkKCCQ(data):
    physical_limitation = 0
    symptom_stability = 0
    symptom_freq = 0
    symptom_burden = 0
    total_symptom_score = 0
    self_efficacy = 0
    quality_of_life = 0
    social_limitation = 0
    overall_summary_score = 0
    cilinical_summary_score = 0

    cnt = 0
    temp = 0
    for ques in ['ques1_a', 'ques1_b', 'ques1_c' ,'ques1_d','ques1_e' ,'ques1_f']:
        if int(data[ques]) != 0: 
            cnt += 1
        temp += int(data[ques])

    if cnt >= 3:
        physical_limitation = 100 * ((temp / cnt) - 1)/4
    
    if int(data['ques2']) != 0:
        if int(data['ques2']) == 6:
            data['ques2'] = 3
        symptom_stability = 100 * (int(data['ques2']) - 1)/4

    cnt = 0
    for ques in ['ques3', 'ques5', 'ques7', 'ques9']:
        if int(data[ques]) != 0:
            cnt += 1

    if  cnt >= 2:
        s3 = max(0, (int(data['ques3']) - 1)/4)
        s5 = max(0, (int(data['ques5']) - 1)/6)
        s7 = max(0, (int(data['ques7']) - 1)/6)
        s9 = max(0, (int(data['ques9']) - 1)/4)

        symptom_freq = (s3+s5+s7+s9)/cnt

    cnt = 0
    if  int(data['ques4']) != 0 or int(data['ques6']) != 0 or int(data['ques8']) != 0:
        if int(data['ques4']) == 6:
            data['ques4'] = 5
        if int(data['ques6']) == 6:
            data['ques6'] = 5
        if int(data['ques8']) == 6:
            data['ques8'] = 5

        for ques in ['ques4', 'ques6', 'ques6']:
            if int(data[ques]) != 0:
                cnt += 1

        symptom_burden = 100 * ((int(data['ques8']) + int(data['ques4']) + data['ques6'])/cnt - 1)/4

    total_symptom_score = (symptom_burden + symptom_freq) / 2

    cnt = 0
    if int(data['ques10']) != 0 or int(data['ques11']) != 0:
        for ques in ['ques11', 'ques10']:
            if int(data[ques]) != 0:
                cnt += 1

        self_efficacy = 100 * ((int(data['ques10']) + int(data['ques11']))/cnt - 1)/4
    

    if  int(data['ques12']) != 0 or int(data['ques13']) != 0 or int(data['ques14']) != 0:
        for ques in ['ques12', 'ques13', 'ques14']:
            if int(data[ques]) != 0:
                cnt += 1

        quality_of_life = 100 * ((int(data['ques12']) + int(data['ques13']) + data['ques14'])/cnt - 1)/4

    cnt = 0
    temp = 0
    for ques in ['ques15_a', 'ques15_b', 'ques15_c' ,'ques15_d']:
        if int(data[ques]) != 0: 
            cnt += 1
        temp += int(data[ques])

    if cnt > 0:
        social_limitation = 100 * ((temp / cnt) - 1)/4

    overall_summary_score = (physical_limitation + total_symptom_score + quality_of_life + social_limitation) / 4
    cilinical_summary_score = (physical_limitation + total_symptom_score) / 2

    kccq_s = {
        "physical_limitation" : physical_limitation,
        "symptom_stability" : symptom_stability,
        "symptom_freq" : symptom_freq,
        "symptom_burden" : symptom_burden,
        "total_symptom_score" : total_symptom_score,
        "self_efficacy" : self_efficacy,
        "quality_of_life" : quality_of_life,
        "social_limitation" : social_limitation,
        "overall_summary_score" : overall_summary_score,
        "cilinical_summary_score" : cilinical_summary_score
    }
    result = ""
    for x in kccq_s:
        result += x.replace("_", " ").capitalize() + ": " +  str(round(kccq_s[x],2)) + "%\n"
    
    p = Patient.objects.get(pk=int(data['patient']))
    d_id = p.doctor.device.device_id
    p_id = p.device.device_id

    result_doc = p.name + " has submitted KCCQ questionnaire \n\n" + result
    result_doc1 = p.name + " \n\n" + result
    send_message(d_id, None, result_doc) 
    patient_message = result 
    print(patient_message)
    
    send_message(p_id, None, result)

    
     
    Notifications(text=result_doc1, doctor=p.doctor).save()
    Notifications(text=result, patient=p).save()

    return result

def notify_doc(data):
    p = Patient.objects.get(pk = int(data['patient']))

    msg = p.name + " has sent an Image"
    send_message(p.doctor.device.device_id, None, msg)