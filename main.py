import json
import helpers
from styles import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Line
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

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
helpers.cleanup()