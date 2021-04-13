##import some pdf stuff
import matplotlib.pyplot as plt
from fpdf import FPDF
from random import randint
from django.conf import settings

from .models import *

def genreport(data):
    name = randint(1, 10000000)
    print(name)

    p = Patient.objects.get(pk = data)

    print(p.name)

    pdf = FPDF(format='letter')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.text(10, 10, 'Name: {}'.format(p.name))
    pdf.text(10, 18, 'Mobile: {}'.format(p.mobile))
    pdf.text(10, 26, 'Gender: {}'.format(p.gender))
    pdf.text(10, 34, 'Age: {}'.format(p.date_of_birth))
    pdf.image('/app/images/profile.png', x = 150, y = 10, w = 60, h = 60, type = '', link = '')

    ##creating and adding charts
    hr = []
    sys = []
    dia = []
    wei = []

    queryset = PatientData.objects.filter(patient=p)
    for query in queryset:
        hr.append(query.heart_rate)
        sys.append(query.systolic)
        dia.append(query.diastolic)
        wei.append(query.weight)

    plt.plot([x for x in range(len(hr))], hr)
    # plt.savefig('hr.png')

    plt.plot([x for x in range(len(hr))], sys)
    # plt.savefig('sys.png')

    plt.plot([x for x in range(len(hr))], dia)
    # plt.savefig('dia.png')

    plt.plot([x for x in range(len(hr))], wei)
    plt.savefig('chart.png')

    pdf.image('chart.png', x = 0, y = 75, w = 220, h = 70, type = '', link = '')
    # pdf.image('sys.png', x = 0, y = 150, w = 220, h = 70, type = '', link = '')
    # pdf.image('dia.png', x = 0, y = 225, w = 220, h = 70, type = '', link = '')
    # pdf.image('wei.png', x = 0, y = 300, w = 220, h = 70, type = '', link = '')

    pdf.output('{}/pdfs/{}.pdf'.format(settings.BASE_DIR, name), 'F')

    return name