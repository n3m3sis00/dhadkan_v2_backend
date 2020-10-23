##import some pdf stuff
import matplotlib.pyplot as plt
from fpdf import FPDF
from random import randint

from .models import *

def genreport(data):
    name = randint(1, 10000000)
    print(name)

    p = Patient.objects.get(pk = data)

    print(p.name)

    pdf = FPDF(format='letter')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Name: {}'.format(p.name))
    pdf.cell(40, 20, 'Mobile: {}'.format(p.mobile))
    pdf.cell(40, 30, 'Gender: {}'.format(p.gender))
    pdf.cell(40, 40, 'Age: {}'.format(p.date_of_birth))

    ##creating and adding charts
    data = [23, 45, 56, 78, 213]
    plt.bar([1,2,3,4,5], data)
    plt.savefig('chart.png')

    pdf.image('chart.png', x = 0, y = 40, w = 100, h = 100, type = '', link = '')


    ## Data Table
    data = [['First name','Last name','Age','City'],
            ['Jules','Smith',34,'San Juan'],
            ['Mary','Ramos',45,'Orlando'],[
            'Carlson','Banks',19,'Los Angeles']
            ]

    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    pdf.ln(0.5)
    
    th = pdf.font_size
    for row in data:
        for datum in row:
            pdf.cell(col_width, 2*th, str(datum), border=1)
        pdf.ln(th)

    pdf.output('/home/codespace/workspace/dhadkan_v3_backend/pdfs/{}.pdf'.format(name), 'F')

    return name