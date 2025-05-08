from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.graphics.shapes import Path
from reportlab.lib.enums import TA_CENTER,TA_LEFT, TA_RIGHT
from testrandom import create_rotated_text_image

# ---- Styles ----
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

# ---- JSON ----
data = {
    "header": {
        "text": [
            "Motivational/Personal Factors",
            "Assessment"
        ]
    }, 
    "footer": {
        "text": [
            "Low agreement"
        ]
    },
    "text": [
        "Excelling as a leader requires not only core abilities or competencies, but also the desire to take on typical leadership duties and responsibilities. Listed below are a number of motivational and personal factors that, along with ability, are essential to understanding leadership potential. Each factor is measured by several items that focus on specific behaviors or attitudes. Your overall rating, along with ratings for each specific behavior or attitude related to each factor, is provided below. The \"All Raters\" category includes all ratings with the exception of your self scores.",
        "An \"*\" indicates only Self ratings were collected for that item. Additionally, the wording of some items in the assessment varies depending on the rater source. For example, the item \"Really cares about the success of the agency\" appeared as \"I really care about the success of my agency\" on the version of the assessment you, the participant, responded to, while the same item appeared as \"He or she really cares about the success of his or her agency\" for all other raters."
    ],
    "charts": [
        {
            "type": "grid",
            "cols": 7,
            "rows": [
                {
                    "colspan": 7,
                    "cols": [
                        {
                            "text": "Organizational Engagement"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": "Displays enthusiasm and excitement about the agency’s work. Exerts effort beyond what is expected spends extra time working to help achieve organizational goals. Demonstrates pride in working for the agency and is supportive of the organization as a whole."
                        },
                        {
                            "type": "bar",
                            "text": "Self",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                                1.1
                            ]
                        },
                        {
                            "type": "bar",
                            "text": "Sup.",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                                4.6
                            ]
                        },
                        {
                            "type": "bar",
                            "text": "Peers",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                                4.8
                            ]
                        },
                        {
                            "type": "bar",
                            "text": "Dir. Rpts.",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                            ]
                        },
                        {
                            "type": "bar",
                            "text": "Others",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                                5.0
                            ]
                        },
                        {
                            "type": "bar",
                            "text": "All Raters",
                            "min": 1.0,
                            "max": 5.0,
                            "data": [
                                4.8
                            ]
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": "Your Score"
                        },
                        {
                            "text": "4.3"
                        },
                        {
                            "text": "4.6"
                        },
                        {
                            "text": "4.8"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.8"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": "Group Average"
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.6"
                        },
                        {
                            "text": "4.7"
                        },
                        {
                            "text": "4.6"
                        },
                        {
                            "text": "4.6"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": "Org. Benchmark"
                        },
                        {
                            "text": "4.1"
                        },
                        {
                            "text": "4.4"
                        },
                        {
                            "text": "4.3"
                        },
                        {
                            "text": "4.4"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.4"
                        }
                    ]
                }
            ]
        },
        {
            "type": "grid",
            "cols": 8,
            "rows": [
                {
                    "cols": [
                        {
                            "text": "Factor Items",
                            "rowspan": "*"
                        },
                        {
                            "text": "1. Volunteers for work when opportunities arise."
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.6"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.7"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                            
                        },
                        {
                            "text": "2. Gets excited thinking or talking about what they can accomplish at work."
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.7"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "3. Puts in a great deal of effort to make sure the work is done."
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.9"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "4. I am excited about going to work each day.*"
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.9"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "5. Is passionate about their work."
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.9"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "6. Speaks highly of the organization."
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "7. Is proud to work for their agency."
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.9"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.9"
                        }
                    ]
                },
                {
                    "cols": [
                        {
                            "text": ""
                        },
                        {
                            "text": "8. Is willing to put in a great deal of effort beyond what is expected to help the agency be successful."
                        },
                        {
                            "text": "4.0"
                        },
                        {
                            "text": "4.5"
                        },
                        {
                            "text": "4.6"
                        },
                        {
                            "text": "--"
                        },
                        {
                            "text": "5.0"
                        },
                        {
                            "text": "4.7"
                        }
                    ]
                }
            ]
        }
    ]
}

# ---- Helper: Create vertical bar drawing ----
def create_vertical_bar(value, min_value, max_value, width=30, height=100, label_color=colors.Color(90/255, 128/255, 184/255)):
    if value is None or value == 0:
        value = min_value
    percent = (value - min_value) / (max_value - min_value) if max_value > min_value else 0
    bar_height = height * percent

    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=None, strokeColor=None))

    for i in range(int(min_value), int(max_value) + 1):
        y = (i - min_value) / (max_value - min_value) * height
        d.add(Line(0, y, width, y, strokeColor=colors.grey, strokeWidth=0.5))

    d.add(Rect(5, 0, width - 10, bar_height, fillColor=label_color, strokeColor=None))
    return d

# ---- Build document ----
from reportlab.lib.units import inch

story = []

# ---- Header row with arc drawing and titles ----
TOTAL_WIDTH = 500

arc_width = 15  # same as first table column width
arc_height = 30

arc_drawing = Drawing(arc_width, arc_height + 10)

path = Path()
path.moveTo(0, arc_height)  # vertical line starts at x=0, shifted upward by 5
path.lineTo(0, 15)              # vertical down, shifted upward by 5
path.curveTo(0, 0, 12, 0, 12, 0)  # bottom-right curve

path.strokeColor = colors.Color(0.15, 0.25, 0.45)
path.strokeWidth = 1.5

arc_drawing.add(path)

heading_inner_table = Table(
    [[arc_drawing, Paragraph('<b><i>%s</i></b>' % data["header"]["text"][0], mainHeading)]],
    colWidths=[arc_width, TOTAL_WIDTH * 0.7 - (arc_width)]
)

assessment_text = Paragraph('<i>%s</i>' % data["header"]["text"][1], assessment)

assessment_line = Drawing(TOTAL_WIDTH * 0.5, 5)
assessment_line.add(Line(0, 2, TOTAL_WIDTH * 0.5, 2, strokeColor=colors.Color(55/255, 90/255, 140/255), strokeWidth=1.5))

assessment_inner_table = Table(
    [
        [assessment_text],
        [assessment_line]
    ],
    colWidths=[TOTAL_WIDTH * 0.5]
)
assessment_inner_table.setStyle(TableStyle([
    # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    # ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 15),
    ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),

    # ('BACKGROUND', (0, 0), (0,1), "YELLOW"),
    # ('TOPPADDING', (0, 0), (0, 1), 10),



    # ('BACKGROUND', (0, 1), (0, 2), "PINK"),
    # ('VALIGN', (0, 1), (-1, -1), "TOP"),
    # ('ALIGN', (0, 1), (-1, -1), "LEFT"),
]))

header_row = [
    [
        heading_inner_table,
        assessment_inner_table
    ]
]

header_table = Table(
    header_row,
    colWidths=[TOTAL_WIDTH * 0.5, TOTAL_WIDTH * 0.5]
)
heading_inner_table.setStyle(TableStyle([
    ('BOTTOMPADDING', (0, 0), (0, 0), 10),
    ('LEFTPADDING', (0, 0), (0, 0), 0),
    ('RIGHTPADDING', (0, 0), (0, 0), 0),
]))

header_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('LEFTPADDING', (0, 0), (0, 0), 0),


    # ('BACKGROUND', (1, 0), (1, 1), "PINK"),
    # ('BACKGROUND', (0, 0), (0, 1), "PINK"),
    ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
    # ('LEFTPADDING', (1, 0), (1, 1), 100),
    # ('BOTTOMMARGIN', (1, 0), (1, 1), 20),
    # ('LEFTPADDING', (0, 0), (0, 0), 0),
    # ('RIGHTPADDING', (0, 0), (0, 0), 20),
    # ('ALIGN', (1, 0), (1, 1), "YELLOW"),
]))
story.append(header_table)
story.append(Spacer(1, 12))
# # ---- Divider line ----
# line = Drawing(TOTAL_WIDTH, 1)
# line.add(Line(0, 0, TOTAL_WIDTH, 0, strokeColor=colors.Color(55/255, 90/255, 140/255), strokeWidth=1))
# story.append(line)

# ---- Description paragraphs ----
paragraph_rows = []
for para_text in data["text"]:
    para = Paragraph(para_text, leftAlign)
    paragraph_rows.append([para])

paragraph_table = Table(paragraph_rows, colWidths=[TOTAL_WIDTH])
paragraph_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
]))

story.append(paragraph_table)
story.append(Spacer(1, 12))

for chartIndex, chart in enumerate(data["charts"]):
    table_data = []
    rowspan_indices = []

    has_bars = any('type' in c and c['type'] == 'bar' for r in chart['rows'] for c in r['cols'])

    first_data_row = None
    for r in chart['rows']:
        if any('type' in c and c['type'] == 'bar' for c in r['cols']):
            first_data_row = r['cols']
            break

    # ---- Prepare header row ----
    header_row = []
    if has_bars and first_data_row:
        for cell in first_data_row:
            if cell.get('type') == 'bar':
                header_row.append(Paragraph(cell.get('text', ''), small_style))
            else:
                header_row.append('')

    # Header row index will be set when we insert the header row later
    header_row_index = None

    # ---- Data rows ----
    first_data_row_table_index = None
    for row_idx, row in enumerate(chart['rows']):
        table_row = []
        for col_idx, cell in enumerate(row['cols']):
            text = cell.get('text', '')

            if cell.get('rowspan') == '*':
                rowspan_indices.append((col_idx, len(table_data)))

            if cell.get('type') == 'bar':
                value = cell.get('data')[0] if cell.get('data') else 0
                bar = create_vertical_bar(value, cell.get('min', 1.0), cell.get('max', 5.0))
                table_row.append(bar)
            else:
                if ( row.get('colspan') ==  chart['cols']) :  
                    styleToUse = heading
                elif( (chart['cols'] == 7 and col_idx == 0) or ( chart['cols'] == 8 and col_idx < 2 ) ) :
                    styleToUse = leftAlign
                else : 
                    styleToUse = small_style

                if cell.get('rowspan') == '*':
                    table_row.append(Image(create_rotated_text_image(text)))
                else : 
                    para = Paragraph(text, styleToUse)
                    table_row.append(para)

        # Before appending the first data row, store its table index
        if row_idx == 0:
            first_data_row_table_index = len(table_data)
        table_data.append(table_row)
        # Insert header row after first data row (row_idx == 0), if needed
        if has_bars and row_idx == 0 and header_row:
            table_data.append(header_row)
            header_row_index = len(table_data) - 1
    # ---- Column widths ----
    TOTAL_WIDTH = 500

    bgBlueCols = []
    bottomBorderRows = []
    if chart['cols'] == 7:
        first_col_ratio = 0.5
        first_col_width = TOTAL_WIDTH * first_col_ratio
        other_cols = chart['cols'] - 1
        other_col_width = (TOTAL_WIDTH - first_col_width) / other_cols
        col_widths = [first_col_width] + [other_col_width] * other_cols

        bgBlueCols = [ 5,3,1 ]

    elif chart['cols'] == 8:
        # First column very small
        first_col_ratio = 0.03
        first_col_width = TOTAL_WIDTH * first_col_ratio

        # Total width we want for first two columns (same as first col of 7-col layout)
        target_width = TOTAL_WIDTH * 0.5

        # Second column gets the remainder
        second_col_width = target_width - first_col_width

        other_cols = chart['cols'] - 2  # 6 remaining columns
        other_col_width = (TOTAL_WIDTH - target_width) / other_cols

        col_widths = [first_col_width, second_col_width] + [other_col_width] * other_cols
        bgBlueCols = [ 6,4,2 ]
        bottomBorderRows = [0,1,2,3,4,5,6,7]

    else:
        first_col_ratio = 0.15
        first_col_width = TOTAL_WIDTH * first_col_ratio
        other_cols = chart['cols'] - 1
        other_col_width = (TOTAL_WIDTH - first_col_width) / other_cols
        col_widths = [first_col_width] + [other_col_width] * other_cols

    # ---- Create table ----
    table = Table(table_data, colWidths=col_widths)

    table_style = TableStyle([
        # ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('BACKGROUND', (-1, 0), (-1, -1), colors.Color(238/255, 221/255, 219/255))
    ])

    for colNum in bgBlueCols :
        table_style.add('BACKGROUND', (colNum, 0), (colNum, -1), colors.Color(188/255, 203/255, 226/255))

    for rowNum in bottomBorderRows :
        table_style.add('LINEBELOW', (1, rowNum), (-1, rowNum),0.5, colors.Color(191/255, 191/255, 191/255))
        table_style.add('BOTTOMPADDING', (0, 0), (-1, -1), 14)


    # Style the first row ("Organizational Engagement") only if it spans all columns
    first_row = chart['rows'][0]
    if 'colspan' in first_row and first_row['colspan'] == chart['cols']:
        table_style.add('BACKGROUND', (0, 0), (-1, 0), colors.Color(55/255, 90/255, 140/255))
        table_style.add('TEXTCOLOR', (0, 0), (-1, 0), colors.white)
        table_style.add('FONTNAME', (0, 0), (-1, 0), 'Helvetica-BoldOblique')


    # ---- Rowspan ----
    for col_idx, start_row in rowspan_indices:
        end_row = len(table_data) - 1
        table_style.add('SPAN', (col_idx, start_row), (col_idx, end_row))
        table_style.add('FONTNAME', (col_idx, start_row), (col_idx, end_row), 'Helvetica-Bold')

    # table_style.add('BACKGROUND', (0, 0), (0, 1), colors.yellow)
    # table_style.add('ROTATE', (0, 0), (0, 1), 90)
    # table_style.add('BACKGROUND', (1, 2), (1, 3), colors.yellow)
    # table_style.add('BACKGROUND', (1, 3), (1, 4), colors.yellow)
    # table_style.add('BACKGROUND', (1, 4), (1, 5), colors.yellow)

    # table_style.add('ALIGN', (1, 0), (1, 1), 'CENTER')
    # table_style.add('ALIGN', (1, 2), (1, 3), 'CENTER')
    # table_style.add('ALIGN', (1, 3), (1, 4), 'CENTER')
    # table_style.add('ALIGN', (1, 4), (1, 5), 'CENTER')

    table.setStyle(table_style)

    story.append(table)
    if(chartIndex == 0) :
        line = Drawing(TOTAL_WIDTH, 2)
        line.add(Line(0, 1, TOTAL_WIDTH, 1, strokeColor=colors.Color(55/255, 90/255, 140/255), strokeWidth=2))
        story.append(line)

# ---- Build PDF ----
# doc = SimpleDocTemplate("combined_charts_output.pdf", pagesize=A4)

doc = SimpleDocTemplate(
    "combined_charts_output.pdf",
    pagesize=A4,
    topMargin=30
)
doc.build(story)

print("PDF created: combined_charts_output.pdf")