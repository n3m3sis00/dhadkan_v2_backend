from rest_framework import serializers
from cvd_portal.models import *
from django.contrib.auth.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class PatientDataSerializer(DynamicFieldsModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all())

    class Meta:
        model = PatientData
        fields = [
            'pk',
            'systolic',
            'diastolic',
            'weight',
            'heart_rate',
            'time_stamp',
            'patient'
        ]


class PatientImageSerializer(DynamicFieldsModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all())

    class Meta:
        model = Image
        fields = [
            'pk',
            'byte',
            'time_stamp',
            'patient'
        ]


class PatientImageNameSerializer(DynamicFieldsModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all())

    class Meta:
        model = Image
        fields = [
            'pk',
            'time_stamp',
            'patient'
        ]


class DeviceSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class PatientSerializer(DynamicFieldsModelSerializer):
    # data = PatientDataSerializer(many=True, read_only=True)
    data = serializers.SerializerMethodField('get_patient_data')
    images = serializers.SerializerMethodField('get_image_data')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    device = DeviceSerializer(read_only=True, many=False)

    class Meta:
        model = Patient
        fields = [
            'pk',
            'name',
            'date_of_birth',
            'address',
            'doctor',
            'email',
            'mobile',
            'data',
            'images',
            'gender',
            'user',
            'device'
        ]

    def get_patient_data(self, obj):
        qset = PatientData.objects.filter(patient_id=obj.pk).\
            order_by('-time_stamp')
        ser = PatientDataSerializer(qset, many=True, read_only=True)
        return ser.data

    def get_image_data(self, obj):
        qset = Image.objects.filter(
            patient_id=obj.pk).order_by('-time_stamp')
        ser = PatientImageNameSerializer(qset, many=True, read_only=True)
        return ser.data


class PatientSerializer1(DynamicFieldsModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'pk',
            'name',
            'date_of_birth',
            # 'address',
            # 'doctor',
            # 'email',
            # 'mobile',
            # 'data',
            'gender',
            # 'user',
            # 'device'
        ]


class DoctorSerializer(DynamicFieldsModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    patients = PatientSerializer1(many=True, read_only=True)
    device = DeviceSerializer(read_only=True, many=False)

    class Meta:
        model = Doctor
        fields = [
            'pk',
            'name',
            'hospital',
            'email',
            'mobile',
            'speciality',
            'designation',
            'user',
            'patients',
            'device'
        ]


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password'
        ]
