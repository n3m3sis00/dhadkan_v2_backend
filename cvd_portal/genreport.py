##import some pdf stuff
import matplotlib.pyplot as plt
from fpdf import FPDF
from random import randint

def genreport(data):
    name = randint(1, 10000000)
    print(name)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('/app/pdfs/{}.pdf'.format(name), 'F')

    return name