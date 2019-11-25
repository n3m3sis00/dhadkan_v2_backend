import os

from cvd_portal.models import *
from cvd_portal.serializers import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from cvd_portal.inform import check
from cvd_portal.fcm_d import send_message

from random import randint
from .inform import send_abcd_notification
from datetime import datetime

class PatientDataCreate(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientDataSerializer

    def post(self, request):
        check(request)
        return super().post(request)


class PatientDataDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = PatientData.objects.all()
    serializer_class = PatientDataSerializer


class PatientImageDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()
    serializer_class = PatientImageSerializer


class PatientImageCreate(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientImageSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def update(self, request, pk):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        d = Doctor.objects.get(pk=data['d_id'])
        p = Patient.objects.get(pk=pk)
        p.doctor = d
        p.save()
        return JsonResponse(
            {"id": p.id}, safe=False, content_type='application/json')


class PatientList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorList(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    def get(self, request):
        if request.GET.get('mobile', '') == '':
            return super(DoctorList, self).get(self, request)
        else:
            try:
                d = Doctor.objects.get(
                    mobile=int(request.GET.get('mobile', '')))
            except:
                return JsonResponse(
                    {"Error": "invalid"},
                    safe=False, content_type='application/json')

            return JsonResponse(
                DoctorSerializer(d).data,
                safe=False, content_type='application/json')


class UserDestroy(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(APIView):
    def post(self, request, format=None):

        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )

        username = data['user']
        password = data['password']

        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            return Response(
               'Username password are not correct',
               status=status.HTTP_404_NOT_FOUND
            )
        response = {}
        response["U_ID"] = user.id

        if Patient.objects.filter(user=user).exists():
            p = Patient.objects.get(user=user)
            response['Type'] = 'patient'
            response['ID'] = p.id
        elif Doctor.objects.filter(user=user).exists():
            d = Doctor.objects.get(user=user)
            response['Type'] = 'doctor'
            response['ID'] = d.pk
        else:
            return Response(
                    'Registration not completed',
                    status=status.HTTP_401_UNAUTHORIZED
                )

        token = Token.objects.get_or_create(user=user)
        response['Token'] = token[0].key
        return JsonResponse(
            response, safe=False, content_type='application/json')


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            Token.objects.filter(user=request.user).delete()
            print("lalalalal")
        except ParseError:
            return Response({'status': 'error'})
        return Response({'status': 'done'})


class PatientOnboarding(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        u = User(username=data['mobile'])
        u.set_password(data['password'])
        u.save()
        response['U_ID'] = u.id

        d = Doctor.objects.get(id=data['doctor'])

        p = Patient(
            name=data['name'],
            mobile=data['mobile'],
            email=data['email'],
            address=data['address'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            user=u,
            doctor=d
            )
        p.save()
        response['ID'] = p.id
        t = Token(user=u)
        t.save()
        response['Token'] = t.key

        return JsonResponse(
            response, safe=False, content_type='application/json')


class DocOnboarding(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        u = User(username=data['mobile'])
        u.set_password(data['password'])
        u.save()
        response['U_ID'] = u.id

        d = Doctor(
            name=data['name'],
            mobile=data['mobile'],
            email=data['email'],
            hospital=data['hospital'],
            # fcm=data['fcm'],
            user=u)
        d.save()
        response['ID'] = d.id

        t = Token(user=u)
        t.save()
        response['Token'] = t.key

        return JsonResponse(
            response, safe=False, content_type='application/json')


class DeviceCRUD(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print("data \n",data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}

        if data['type'] == 'doctor':
            d = Doctor.objects.get(pk=int(data['id']))
            try:
                if d.device is not None and d.device.device_id == data['fcm']:
                    _id = d.device.id
                else:
                    dev = Device(device_id=data['fcm'])
                    dev.save()
                    d.device = dev
                    d.save()
                    _id = dev.id

            except:
                pass

        elif data['type'] == 'patient':
            p = Patient.objects.get(pk=int(data['id']))
            print("Device crud api : value of p\n",p)
            try:
                if p.device is not None and data['fcm'] == p.device.id:
                    _id = p.device.id
                    print("if")
                else:
                    dev = Device(device_id=data['fcm'])
                    dev.save()
                    p.device = dev
                    p.save()
                    _id = dev.id
                    print("else")
            except:
                pass
        else:
            return Response(
                'Server Error',
                status=status.HTTP_401_UNAUTHORIZED
            )

        response['pk'] = _id
        return JsonResponse(
            response, safe=False, content_type='application/json')


class NotificationCRUD(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        p_id = data['p_id']
        p = Patient.objects.get(pk=p_id)
        msg = data['message']
        _to = data['to']
        _from = data['from']
        response['response'] = send_message(_to, _from, msg)
        Notifications(text=msg, patient=p).save()
        return JsonResponse(
            response, safe=False, content_type='application/json')


class MedicineCRUD(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        p_id = data['p_id']
        p = Patient.objects.get(pk=p_id)
        msg = data['message']
        _to = data['to']
        _from = data['from']
        response['response'] = send_message(_to, _from, msg)
        Notifications(text=msg, patient=p).save()
        return JsonResponse(
            response, safe=False, content_type='application/json')



class gen_otp(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        mobile = data['user']
        otp = randint(1000, 9999)
        u = User.objects.get(username=mobile)
        print(u)
        if u is None:
            response['message'] = "Mobile number not registered"
            return JsonResponse(
                response,
                safe=False, content_type='application/json', status=404)
        OTP.objects.filter(user=u).delete()
        if Patient.objects.filter(user=u).exists():
            p = Patient.objects.get(user=u)
            o = OTP(otp=otp, user_type="Patient", user_type_id=p.id, user=u)
            o.save()
            response['otp_id'] = o.id
            send_message(p.device.device_id, None, str(otp))
            return JsonResponse(
                response,
                safe=False, content_type='application/json')

        elif Doctor.objects.filter(user=u).exists():
            d = Doctor.objects.get(user=u)
            o = OTP(otp=otp, user_type="Doctor", user_type_id=d.id, user=u)
            o.save()
            response['otp_id'] = o.id
            send_message(d.device.device_id, None, str(otp))
            return JsonResponse(
                response,
                safe=False, content_type='application/json')
        response['message'] = "Not Registered"
        return JsonResponse(
            response,
            safe=False, content_type='application/json', status=404)


class verify_otp(APIView):
    def post(self, request, format=None):
        # print("yo")
        try:
            data = request.data
            print(data)
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        response = {}
        new_pass = data['new_pass']
        # print(new_pass)
        otp = int(data['otp'])
        o = OTP.objects.get(pk=data['otp_id'])
        # print(o)
        print(o.otp)
        print(otp)
        if o.otp != otp:
            response['message'] = "OTP does not match"
            return JsonResponse(
                response,
                safe=False, content_type='application/json', status=401)
        response["U_ID"] = o.user_id
        print(response)
        u = o.user
        u.set_password(new_pass)
        u.save()

        if o.user_type == "Patient":
            p = Patient.objects.get(pk=o.user_type_id)
            response['Type'] = 'patient'
            response['ID'] = p.id
        elif o.user_type == "Doctor":
            d = Doctor.objects.get(pk=o.user_type_id)
            response['Type'] = 'doctor'
            response['ID'] = d.pk
        else:
            o.delete()
            return Response(
                    'Registration not completed',
                    status=status.HTTP_401_UNAUTHORIZED
                )

        Token.objects.filter(user=o.user).delete()
        token = Token.objects.get_or_create(user=o.user)
        response['Token'] = token[0].key
        o.delete()
        return JsonResponse(
            response,
            safe=False, content_type='application/json')


class patient_notification(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        p = Patient.objects.get(pk=pk)
        nl = Notifications.objects.filter(patient=p).order_by('-time_stamp')
        print(nl)
        print(p)
        print(p.name)
        response = {
            "notifications": []
        }
        for n in nl:
            no = {"text": ""}
            no["text"] = n.text
            response["notifications"].append(no)
        return JsonResponse(
            response,
            safe=False, content_type='application/json')


class doctor_notification(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        d = Doctor.objects.get(pk=pk)
        nl = Notifications.objects.filter(doctor=d).order_by('-time_stamp')
        response = {
            "notifications": []
        }
        for n in nl:
            no = {"text": ""}
            no["text"] = n.text
            response["notifications"].append(no)
        print(response)
        return JsonResponse(
            response,
            safe=False, content_type='application/json')


class Classify(APIView):

    def post(self,request,format=None):
        print("hi____________________________")
        print(request.POST['medicine'])
        try:
            upload = request.FILES['photo']
            extension =  upload.name.split(".")[1]
            filename = "{}".format(upload.name)
            mobile_ = request.POST['mobile']

            with open("/dhadkan_v3_backend-0.0.2/"+filename, 'wb+') as destination:
                for chunk in upload.chunks():
                    destination.write(chunk)

            send_abcd_notification([], mobile_)


        except MultiValueDictKeyError:
            print("no medicine photo ")

        try:
            medicine = request.POST['medicine']
            data_ = medicine.split(",")
            mobile_ = request.POST['mobile']
            print(mobile_)
            send_abcd_notification(data_, mobile_)
            print("Medicine name Given")
        except MultiValueDictKeyError:
            print("no medicine name")

        response = {
            "text_upload": "Hi there"
        }
        return JsonResponse(
            response,
            safe=False, content_type='application/json')

class Remind(APIView):

    def post(self,request,format=None):
        try:
            data = request.data
            print(data)
        except ParseError:
            return JsonResponse({"message":"please set it again"}, safe=False, content_type='application/json')

        text = data['text']
        print(data["date"])
        time = datetime.strptime(data["date"], "%d/%m/%Y") 
        print(time)
        user = Patient.objects.get(pk=int(data["pk"]))
        repeat = data["repeat"]
        freq = data["frequency"]

        rem = Reminder(text = text, patient=user, repeat = repeat, time = time, frequency = freq)
        rem.save()
        return JsonResponse({"message":"Reminder scheduled"}, safe=False, content_type='application/json')


class PatientReminder(APIView):

    def post(self,request,format=None):
        try:
            data = request.data
        except ParseError:
            print("something is wrong")
            return JsonResponse({"message":"please try again"}, safe=False, content_type="application/json")

        pat = Patient.objects.get(pk = int(data["pk"]))

        reminders = Reminder.objects.filter(patient = pat)
        context = []
        for rem in reminders:
            context.append({
                "text":rem.text,
                "date":rem.time,
                "id":rem.id
                })

        return JsonResponse({"message":context},safe=False, content_type="application/json")


