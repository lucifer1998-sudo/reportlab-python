from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT, TA_RIGHT
from reportlab.lib import colors

styles = getSampleStyleSheet()
small_style = styles['Normal'].clone('small_style')
small_style.fontSize = 8
small_style.leading = 10
small_style.alignment = TA_CENTER

leftAlign = styles['Normal'].clone('small_style')
leftAlign.fontSize = 9
leftAlign.leading = 11
leftAlign.alignment = TA_LEFT

heading = styles['Normal'].clone('small_style')
heading.fontSize = 12
heading.leading = 16
heading.alignment = TA_LEFT
heading.textColor = "WHITE"
heading.fontName = "Helvetica-BoldOblique"

mainHeading = styles['Normal'].clone('small_style')
mainHeading.fontSize = 16
mainHeading.leading = 18
mainHeading.alignment = TA_LEFT
mainHeading.textColor =  colors.Color(55/255, 90/255, 140/255)
mainHeading.fontName = "Helvetica-BoldOblique"

assessment = styles['Normal'].clone('small_style')
assessment.fontSize = 10
assessment.leading = 10
assessment.alignment = TA_RIGHT
assessment.textColor =  colors.Color(55/255, 90/255, 140/255)
assessment.fontName = "Helvetica-BoldOblique"


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
