import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhadkan.settings")
import django
from import_export import resources


django.setup()

from cvd_portal.models import PatientData, Patient

class PatientResource(resources.ModelResource):
    class Meta:
        model = PatientData


if __name__ == "__main__" :
    Patient_resource = PatientResource()
    dataset = Patient_resource.export()
    print(dataset.csv)



