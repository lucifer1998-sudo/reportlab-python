import json
from reportlab.pdfgen import canvas
import textwrap
import helpers



with open("data/sample.json") as f:
    data = json.load(f)

# coordinate system:
#   y
#   |
#   |   page
#   |
#   |
#   0-------x

# create a Canvas object with a filename
c = canvas.Canvas("reports/sample.pdf", pagesize=(595.27, 841.89))  # A4 pagesize
c.setTitle(data['title'])

c.setFont("Helvetica-Bold", 24)
c.setFillColor("darkgray")
sections = data['sections']
loopIndex = 0
for section in sections:
    print(loopIndex)

    helpers.drawHeaderAndText(section, c)
    
    if(section['charts'][0]['type'] == 'box_and_whisker'):
        chart_path = helpers.boxAndWhiskerChart(section['charts'][0])
        img_x = 150
        img_y = 300
        img_width = 300
        img_height = 400
        c.drawImage(chart_path, img_x, img_y, width=img_width, height=img_height)
    c.showPage()
    loopIndex = loopIndex + 1

c.save()