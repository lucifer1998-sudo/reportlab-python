import os
import uuid
import textwrap
import numpy as np
from styles import *
import matplotlib.pyplot as plt
from reportlab.lib import colors
from textRotation import VerticalText
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import navy, black
from reportlab.platypus import Image as RLImage
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.graphics.shapes import Drawing, Rect, Line, Path
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer

def boxAndWhiskerChart(chart_data, doc, story):
    data = chart_data['data']
    legend_labels = chart_data.get('legend', {}).get('text', ["Min", "Max", "Mean", "Middle 50%"])

    chart_width_in = 14.5 
    chart_height_in = len(data) * 0.6 + 1.5

    fig, ax = plt.subplots(figsize=(chart_width_in, chart_height_in))

    y_spacing = 1.5
    for i, item in enumerate(data):
        y = (len(data) - i) * y_spacing

        min_val = item["min"]
        max_val = item["max"]
        q1, q3 = item["middle_50"]
        mean = item["mean"]

        ax.hlines(y, min_val, max_val, color='black', linewidth=2)
        cap_height = 0.4
        ax.vlines(min_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)
        ax.vlines(max_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)

        ax.barh(y, q3 - q1, left=q1, height=0.6, color='steelblue', alpha=0.7, edgecolor='none')

        ax.plot(mean, y, 'o',
                markersize=10,
                markerfacecolor='black',
                markeredgecolor='white',
                markeredgewidth=1.5)

    
    y_positions = [(len(data) - i) * y_spacing for i in range(len(data))]
    ax.set_yticks(y_positions)
    ax.set_yticklabels([item["competency"] for item in data], fontsize=18, weight='bold')

    
    all_mins = [item["min"] for item in data]
    all_maxs = [item["max"] for item in data]

    x_min = min(all_mins) - 0.2
    data_max = max(all_maxs)

    tick_max = int(np.ceil(data_max))
    x_min_int = int(np.floor(x_min))

    ax.set_xlim(x_min, tick_max)
    custom_ticks = list(range(x_min_int, tick_max + 1))
    ax.set_xticks(custom_ticks)

    
    all_raters_x = tick_max + 0.2
    benchmark_x = tick_max + 1.2

    for i, item in enumerate(data):
        y = (len(data) - i) * y_spacing
        ax.text(all_raters_x + 0.5, y, f"{item['all_raters']:.1f}", va='top', ha='center', fontsize=18)
        ax.text(benchmark_x + 0.5, y, f"{item['benchmark']:.1f}", va='top', ha='center', fontsize=18)


    
    for spine in ['left', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)

    ax.spines['top'].set_visible(True)
    ax.spines['top'].set_position(('outward', 0))
    ax.spines['top'].set_linewidth(1)
    ax.spines['top'].set_color('black')

    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=5, width=1, direction='out', labelsize=14)
    ax.tick_params(axis='y', length=0)

    

    headers = chart_data['headers']
    text_for_benchmark = next((h["text"] for h in headers if h["id"] == "benchmark"), None)
    text_for_all_raters = next((h["text"] for h in headers if h["id"] == "all_raters"), None)

    col_width_chars = 10
    text_for_all_raters = "\n".join(textwrap.wrap(text_for_all_raters, width=col_width_chars))
    text_for_benchmark = "\n".join(textwrap.wrap(text_for_benchmark, width=col_width_chars))

    header_y = ax.get_ylim()[1] + 0.1
    ax.text(all_raters_x + 0.5, header_y, text_for_all_raters, fontsize=18, va='bottom', ha='center')
    ax.text(benchmark_x + 0.5, header_y, text_for_benchmark, fontsize=18, va='bottom', ha='center')

    

    
    legend_y = min(y_positions) - y_spacing * 1.5

    
    legend_min = x_min_int + 0.5
    legend_max = tick_max - 0.5
    legend_q1 = legend_min + (legend_max - legend_min) * 0.25
    legend_q3 = legend_min + (legend_max - legend_min) * 0.75
    legend_mean = (legend_q1 + legend_q3) / 2

    
    ax.hlines(legend_y, legend_min, legend_max, color='black', linewidth=2)
    
    ax.vlines(legend_min, legend_y - 0.3, legend_y + 0.3, color='black', linewidth=2)
    ax.vlines(legend_max, legend_y - 0.3, legend_y + 0.3, color='black', linewidth=2)
    
    ax.barh(legend_y, legend_q3 - legend_q1, left=legend_q1, height=0.6,
            color='steelblue', alpha=0.7, edgecolor='none')
    
    ax.plot(legend_mean, legend_y, 'o',
            markersize=10,
            markerfacecolor='black',
            markeredgecolor='white',
            markeredgewidth=1.5)

    ax.text(legend_min - 0.1, legend_y, legend_labels[0], ha='right', va='center', fontsize=11)
    ax.text(legend_max + 0.1, legend_y, legend_labels[1], ha='left', va='center', fontsize=11)
    ax.text(legend_mean, legend_y - 0.3, legend_labels[2], ha='center', va='top', fontsize=11)
    ax.text((legend_q1 + legend_q3) / 2, legend_y + 0.3, legend_labels[3], ha='center', va='bottom', fontsize=11)

    

    plt.tight_layout()
    chart_path = "reports/chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    img = PILImage.open(chart_path)
    img_width_px, img_height_px = img.size

    
    max_width_pt = doc.width
    max_height_pt = doc.height

    
    img_width_pt = img_width_px * 72 / 300
    img_height_pt = img_height_px * 72 / 300

    
    width_ratio = max_width_pt / img_width_pt
    height_ratio = max_height_pt / img_height_pt
    scale = min(width_ratio, height_ratio) * 0.82

    img_width_pt *= scale
    img_height_pt *= scale

    chart_img = RLImage(chart_path, width=img_width_pt, height=img_height_pt)
    story.append(chart_img)


def drawHeaderAndText(section, c) : 
    page_width, page_height = A4
    x_left = 50
    y_top = 780
    xAxis = 50
    yAxis = 780


    if(isinstance(section['header'], str)) : 
        c.setFont("Helvetica-BoldOblique", 16)
        c.setFillColor(navy)
        c.drawString(xAxis, yAxis, section['header'])
        c.setStrokeColor(navy)
        c.setLineWidth(2)
        yAxis = yAxis - 10
        c.line(50, yAxis, 550, yAxis)

    else : 

        
        left_header = section['header']['text'][0]
        c.setFont("Helvetica-BoldOblique", 16)
        c.setFillColor(navy)
        c.drawString(x_left, y_top, left_header)

        
        right_header = section['header']['text'][1]
        c.setFont("Helvetica-Oblique", 12)
        c.drawRightString(page_width - 100, y_top + 12, right_header)

        
        left_text_width = stringWidth(left_header, "Helvetica-BoldOblique", 16)

        corner_radius = 6
        corner_x = x_left - corner_radius
        corner_y = y_top - 2

        c.setStrokeColor(navy)
        c.setLineWidth(1.5)


        
        c.arc(
            corner_x, 
            corner_y - corner_radius, 
            corner_x + 2 * corner_radius, 
            corner_y + corner_radius, 
            startAng=180, 
            extent=90
        )

        line_start_x = x_left + left_text_width + 4
        baseline_y = y_top + 4

        c.line(line_start_x, baseline_y, page_width - 50, baseline_y)

    
    c.setFont("Helvetica", 10)
    c.setFillColor(black)

    y = y_top - 30
    wrap_width = 95

    for text in section['text']:
        wrapped_lines = textwrap.wrap(text, width=wrap_width)
        for line in wrapped_lines:
            c.drawString(x_left, y, line)
            y -= 14
        y -= 10


def drawHeaderedTable(data, story) :
    TOTAL_WIDTH = 500

    arc_width = 15
    arc_height = 30

    arc_drawing = Drawing(arc_width, arc_height + 10)

    path = Path()
    path.moveTo(0, arc_height)
    path.lineTo(0, 15)
    path.curveTo(0, 0, 12, 0, 12, 0)

    path.strokeColor = colors.Color(0.15, 0.25, 0.45)
    path.strokeWidth = 1.5

    arc_drawing.add(path)

    heading_text = data["header"]["text"][0]
    text_width = stringWidth(heading_text, mainHeading.fontName, mainHeading.fontSize)
    heading_width = arc_width + text_width + 20


    if heading_width > TOTAL_WIDTH * 0.75:
        heading_width = TOTAL_WIDTH * 0.75

    assessment_width = TOTAL_WIDTH - heading_width

    heading_inner_table = Table(
        [[arc_drawing, Paragraph('<b><i>%s</i></b>' % heading_text, mainHeading)]],
        colWidths=[arc_width, heading_width - arc_width]
    )

    assessment_text = Paragraph('<i>%s</i>' % data["header"]["text"][1], assessment)

    assessment_line = Drawing(assessment_width, 5)
    assessment_line.add(Line(0, 2, assessment_width, 2, strokeColor=colors.Color(55/255, 90/255, 140/255), strokeWidth=1.5))

    assessment_inner_table = Table(
        [
            [assessment_text],
            [assessment_line]
        ],
        colWidths=[assessment_width]
    )
    assessment_inner_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    header_row = [
        [
            heading_inner_table,
            assessment_inner_table
        ]
    ]

    header_table = Table(
        header_row,
        colWidths=[heading_width, assessment_width]
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
        ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))


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


def create_rotated_text_image(text, img_width=100, img_height=40, font_size=48):
    bg_color = "white"
    text_color = "black"

    image = PILImage.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2
    draw.text((x, y), text, fill=text_color, font=font)
    rotated_image = image.rotate(90, expand=True)
    output_path = f"assets/rotated_{uuid.uuid4().hex[:8]}.png"
    rotated_image.save(output_path, dpi=(300, 300))
    return output_path
    
def drawGrids(chart, chartIndex, story) :

    table_data = []
    rowspan_indices = []

    has_bars = any('type' in c and c['type'] == 'bar' for r in chart['rows'] for c in r['cols'])
    first_data_row = None
    for r in chart['rows']:
        if any('type' in c and c['type'] == 'bar' for c in r['cols']):
            first_data_row = r['cols']
            break
    header_row = []
    if has_bars and first_data_row:
        for cell in first_data_row:
            if cell.get('type') == 'bar':
                header_row.append(Paragraph(cell.get('text', ''), small_style))
            else:
                header_row.append('')
                
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
                    table_row.append(VerticalText(text,width=60,height=60))
                else :
                    para = Paragraph(text, styleToUse)
                    table_row.append(para)
        if row_idx == 0:
            first_data_row_table_index = len(table_data)
        table_data.append(table_row)
        if has_bars and row_idx == 0 and header_row:
            table_data.append(header_row)
            header_row_index = len(table_data) - 1
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
        first_col_ratio = 0.03
        first_col_width = TOTAL_WIDTH * first_col_ratio
        target_width = TOTAL_WIDTH * 0.5
        second_col_width = target_width - first_col_width
        other_cols = chart['cols'] - 2
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
    table = Table(table_data, colWidths=col_widths)
    table_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('BACKGROUND', (-1, 0), (-1, -1), colors.Color(238/255, 221/255, 219/255)),
    ])
    for colNum in bgBlueCols :
        table_style.add('BACKGROUND', (colNum, 0), (colNum, -1), colors.Color(188/255, 203/255, 226/255))
    for rowNum in bottomBorderRows :
        table_style.add('LINEBELOW', (1, rowNum), (-1, rowNum),0.5, colors.Color(191/255, 191/255, 191/255))
        table_style.add('BOTTOMPADDING', (0, 0), (-1, -1), 14)
    first_row = chart['rows'][0]
    if 'colspan' in first_row and first_row['colspan'] == chart['cols']:
        table_style.add('BACKGROUND', (0, 0), (-1, 0), colors.Color(55/255, 90/255, 140/255))
        table_style.add('TEXTCOLOR', (0, 0), (-1, 0), colors.white)
        table_style.add('FONTNAME', (0, 0), (-1, 0), 'Helvetica-BoldOblique')
    for col_idx, start_row in rowspan_indices:
        end_row = len(table_data) - 1
        table_style.add('SPAN', (col_idx, start_row), (col_idx, end_row))
        table_style.add('VALIGN', (col_idx, start_row), (col_idx, end_row), 'CENTER')
        table_style.add('ALIGN', (col_idx, start_row), (col_idx, end_row), 'RIGHT')
    table.setStyle(table_style)
    story.append(table)
    if(chartIndex == 0) :
        line = Drawing(TOTAL_WIDTH, 2)
        line.add(Line(0, 1, TOTAL_WIDTH, 1, strokeColor=colors.Color(55/255, 90/255, 140/255), strokeWidth=2))
        story.append(line)

def drawBarChart(chart, doc, story):
    data = chart['data']
    
    
    competencies = [item["competency"] for item in data]
    scores = [item["score"] for item in data]
    benchmarks = [item["benchmark"] for item in data]

    
    bar_colors = [
        "#AEC6CF" if item.get("barColor") == "lightblue" else "#1F3A5F"
        for item in data
    ]

    y_pos = np.arange(len(competencies))

    
    fig, ax = plt.subplots(figsize=(11, 9))

    bars = ax.barh(y_pos, scores, color=bar_colors, edgecolor='none')
    ax.scatter(benchmarks, y_pos, marker='D', color='darkorange', s=80, label='Benchmark')

    ax.set_xlim(1, 5)
    ax.set_xticks(range(1, 6))

    
    headers = chart['headers']
    text_for_benchmark = next((h["text"] for h in headers if h["id"] == "benchmark"), "")
    text_for_average_raters = next((h["text"] for h in headers if h["id"] == "all_raters"), "")

    
    col_width_chars = 10
    text_for_average_raters = "\n".join(textwrap.wrap(text_for_average_raters, width=col_width_chars))
    text_for_benchmark = "\n".join(textwrap.wrap(text_for_benchmark, width=col_width_chars))

    
    avg_x = 5.6
    benchmark_x = 6.6
    header_y = -1.9

    
    ax.text(avg_x, header_y, text_for_average_raters, fontsize=12, ha='center', va='top', linespacing=1.4)
    ax.text(benchmark_x, header_y, text_for_benchmark, fontsize=12, ha='center', va='top')

    
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', which='both', direction='out', length=5, width=1.5, top=True, bottom=False)

    ax.invert_yaxis()

    
    for spine in ['bottom', 'left', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax.spines['top'].set_linewidth(1.5)

    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(competencies, fontsize=12, weight='bold')
    ax.tick_params(axis='y', length=0, which='both', left=False)

    
    for i, (score, benchmark) in enumerate(zip(scores, benchmarks)):
        ax.text(avg_x, i, f"{score:.1f}", va='center', ha='center', fontsize=12)
        ax.text(benchmark_x, i, f"{benchmark:.1f}", va='center', ha='center', fontsize=12)

    
    legend_y = -0.08
    ax.plot([0.03, 0.17], [legend_y, legend_y], color="#1F3A5F", lw=12, transform=ax.transAxes, clip_on=False)
    ax.text(0.1, legend_y - 0.03, "Competencies", ha='center', va='top', fontsize=11, transform=ax.transAxes)

    ax.plot([0.40, 0.60], [legend_y, legend_y], color="#AEC6CF", lw=12, transform=ax.transAxes, clip_on=False)
    ax.text(0.5, legend_y - 0.03, "Motivational/Personal", ha='center', va='top', fontsize=11, transform=ax.transAxes)

    ax.scatter(0.9, legend_y, marker='D', s=80, color="darkorange", transform=ax.transAxes, clip_on=False)
    ax.text(0.9, legend_y - 0.03, "Benchmark", ha='center', va='top', fontsize=11, transform=ax.transAxes)

    plt.tight_layout(rect=[0, 0.15, 1, 1])

    chart_path = "reports/bar-chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()

    img = PILImage.open(chart_path)
    img_width_px, img_height_px = img.size

    
    max_width_pt = doc.width
    max_height_pt = doc.height

    
    img_width_pt = img_width_px * 72 / 300
    img_height_pt = img_height_px * 72 / 300

    
    width_ratio = max_width_pt / img_width_pt
    height_ratio = max_height_pt / img_height_pt
    scale = min(width_ratio, height_ratio) * 0.82

    img_width_pt *= scale
    img_height_pt *= scale

    chart_img = RLImage(chart_path, width=img_width_pt, height=img_height_pt)
    story.append(chart_img)
    return chart_path

def set_pdf_metadata_factory(data):
    def set_pdf_metadata(canvas, doc):
        canvas.setTitle(data['title'])
    return set_pdf_metadata

def cleanup() :
    os.remove('reports/bar-chart.png')
    os.remove('reports/chart.png')