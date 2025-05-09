import os
import sys
import json
import helpers
from styles import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Line
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

def exit_with_error(message):
    print(f"❌ Error: {message}")
    sys.exit(1)


if len(sys.argv) < 2:
    exit_with_error("\nPlease provide the input JSON path \nUsage: python main.py path/to/data.json \n")

json_path = sys.argv[1]

if not os.path.exists(json_path):
    exit_with_error(f"File not found: {json_path}")

try:
    with open(json_path) as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    exit_with_error(f"Invalid JSON file: {e}")


if "title" not in data:
    exit_with_error("Missing 'title' key in JSON.")

if "sections" not in data or not isinstance(data["sections"], list):
    exit_with_error("Missing or invalid 'sections' list in JSON.")


os.makedirs("reports", exist_ok=True)

output_pdf = f"reports/{data['title']}.pdf"
doc = SimpleDocTemplate(
    output_pdf,
    pagesize=A4,
    topMargin=30,
    bottomMargin=30,
    leftMargin=40,
    rightMargin=40
)

story = []


for section_index, section in enumerate(data['sections']):
    try:
        header = section['header']

        if isinstance(header, str):
            story.append(Paragraph(header, title_style))
            page_width, page_height = A4
            line = Drawing(page_width - doc.leftMargin - doc.rightMargin, 2)
            line.add(Line(0, 1, page_width - doc.leftMargin - doc.rightMargin, 1, strokeColor=colors.darkgrey, strokeWidth=3))
            story.append(line)
        else:
            helpers.drawHeaderedTable(section, story)

        for para in section.get('text', []):
            story.append(Paragraph(para, body_style))

        for chartIndex, chart in enumerate(section.get('charts', [])):
            chart_type = chart.get('type')
            if chart_type == 'box_and_whisker':
                helpers.boxAndWhiskerChart(chart, doc, story)
            elif chart_type == 'grid':
                helpers.drawGrids(chart, chartIndex, story)
            elif chart_type == 'bar':
                helpers.drawBarChart(chart, doc, story)
            else:
                print(f"⚠️  Unknown chart type '{chart_type}' in section {section_index}")
    except Exception as e:
        print(f"⚠️  Failed to process section {section_index}: {e}")

    story.append(PageBreak())

try:
    doc.build(story, onFirstPage=helpers.set_pdf_metadata_factory(data))
    helpers.cleanup()
    output_path = os.path.abspath(output_pdf)
    print(f"✅ PDF report generated at: {output_path}")
except Exception as e:
    exit_with_error(f"Failed to generate PDF: {e}")