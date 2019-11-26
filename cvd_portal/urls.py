from django.conf.urls import url
from rest_framework.authtoken import views
from cvd_portal.views import *
urlpatterns = [
    #Classification
    url(r'api/classify$', Classify.as_view()),
    url(r'api/medicine$', MedicineCRUD.as_view()),
    url(r'api/reminder$', Remind.as_view()),
    url(r'api/getreminders$', PatientReminder.as_view()),
    url(r'api/delreminder$', DelReminder.as_view()),
    url(r'api/ocr$', Ocr.as_view()),

    #view patient data get
    url(r'api/patient/(?P<pk>[0-9]+)$', PatientDetail.as_view()),
    url(r'api/patient$', PatientList.as_view()),
    url(r'api/doctor/(?P<pk>[0-9]+)$', DoctorDetail.as_view()),
    #lIST OF DOCTORS (GET)
    url(r'api/doctor$', DoctorList.as_view()),
    # url(r'api/user$', UserCreate.as_view()),
    url(r'api/user/(?P<pk>[0-9]+)$', UserDestroy.as_view()),
    url(r'api/data/(?P<pk>[0-9]+)$', PatientDataDetail.as_view()),
    url(r'api/data$', PatientDataCreate.as_view()),
    url(r'api/image/(?P<pk>[0-9]+)$', PatientImageDetail.as_view()),
    url(r'api/image$', PatientImageCreate.as_view()),
    #Login API (post)
    url(r'api/login$', Login.as_view()),
    #LOGOUT api
    url(r'api/logout$', Logout.as_view()),
    url(r'api/onboard/doc$', DocOnboarding.as_view()),
    url(r'api/onboard/patient$', PatientOnboarding.as_view()),
    url(r'api/device$', DeviceCRUD.as_view()),
    url(r'api/notification$', NotificationCRUD.as_view()),
    url(r'api/gen_otp$', gen_otp.as_view()),
    url(r'api/verify_otp$', verify_otp.as_view()),
    url(
        r'api/notification/patient/(?P<pk>[0-9]+)$',
        patient_notification.as_view()),
    url(
        r'api/notification/doctor/(?P<pk>[0-9]+)$',
        doctor_notification.as_view())
]
