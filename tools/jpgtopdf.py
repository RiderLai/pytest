"""jpg转pdf"""


import os
import sys
from reportlab.pdfgen import canvas

c = canvas.Canvas(sys.argv[1] + '\\anime.pdf')
folders = os.listdir(sys.argv[1])
for folder in folders:
    files = os.listdir(sys.argv[1] + '\\' + folder)
    for file in files:
        c.drawImage(sys.argv[1] + '\\' + folder + '\\'+file, 100, 50, width=400, height=600)
        c.showPage()

c.save()
