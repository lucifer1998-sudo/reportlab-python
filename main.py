import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line
import helpers
from reportlab.lib import colors

from reportlab.platypus import Image as RLImage
from PIL import Image as PILImage

with open("data/sample.json") as f:
    data = json.load(f)

doc = SimpleDocTemplate(
    f"reports/{data['title']}.pdf",
    pagesize=A4,
    topMargin=30,
    bottomMargin=30,
    leftMargin=40,
    rightMargin=40
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=22,
    textColor=colors.Color(56/255, 56/255, 56/255),
    spaceAfter=10
)
subtitle_style = ParagraphStyle(
    'SubtitleStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=12,
    alignment=2,  # right-aligned
    spaceAfter=6
)
body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=9,
    leading=14,
    spaceAfter=10,
    textColor=colors.Color(0/255, 45/255, 91/255)
)

story = []

for section in data['sections']:
    header = section['header']

    
    if isinstance(header, str):
        story.append(Paragraph(header, title_style))
        page_width, page_height = A4
        line = Drawing(page_width - doc.leftMargin - doc.rightMargin, 2)
        line.add(Line(0, 1, page_width - doc.leftMargin - doc.rightMargin, 1, strokeColor=colors.darkgrey, strokeWidth=3))
        story.append(line)
    else:
        helpers.drawHeaderedTable(section, story)

    
    for para in section['text']:
        story.append(Paragraph(para, body_style))

    for chartIndex, chart in enumerate(section['charts']) : 
        if chart['type'] == 'box_and_whisker':
            helpers.boxAndWhiskerChart(chart, doc, story)
        elif (chart['type'] == 'grid') :
            helpers.drawGrids(chart, chartIndex, story)
        elif (chart['type'] == 'bar') :
            helpers.drawBarChart(chart, doc, story)

    story.append(PageBreak())

doc.build(story, onFirstPage=helpers.set_pdf_metadata_factory(data))