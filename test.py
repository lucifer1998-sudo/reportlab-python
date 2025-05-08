import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line
import helpers
from reportlab.lib import colors

# Load data
with open("data/sample.json") as f:
    data = json.load(f)

# PDF settings
doc = SimpleDocTemplate(
    "reports/sample_platypus.pdf",
    pagesize=A4,
    topMargin=30,
    bottomMargin=30,
    leftMargin=40,
    rightMargin=40
)

# Styles
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

# Build story
story = []

for section in data['sections']:
    header = section['header']

    # Header
    if isinstance(header, str):
        story.append(Paragraph(header, title_style))
        page_width, page_height = A4
        line = Drawing(page_width - doc.leftMargin - doc.rightMargin, 2)  # 2 points high
        line.add(Line(0, 1, page_width - doc.leftMargin - doc.rightMargin, 1, strokeColor=colors.darkgrey, strokeWidth=3))
        story.append(line)
    else:
        helpers.drawHeaderedTable(section, story)

    # Paragraphs
    for para in section['text']:
        story.append(Paragraph(para, body_style))

    # Chart
    # if section['charts'] and section['charts'][0]['type'] == 'box_and_whisker':
    #     chart_path = helpers.boxAndWhiskerChart(section['charts'][0])
    #     story.append(Spacer(1, 20))
    #     story.append(Image(chart_path, width=300, height=400))

    for chartIndex, chart in enumerate(section['charts']) : 
        if chart['type'] == 'box_and_whisker':
            chart_path = helpers.boxAndWhiskerChart(chart)
            story.append(Spacer(1, 20))
            story.append(Image(chart_path, width=300, height=400))
        elif (chart['type'] == 'grid') :
            helpers.drawGrids(chart, chartIndex, story)



    story.append(PageBreak())

# Generate PDF
doc.build(story)