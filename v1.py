import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


def boxAndWhiskerChart(data) :

    
    fig, ax = plt.subplots(figsize=(10, len(data) * 0.6))  # ~0.6 inch per row

    y_spacing = 1.5  # Space between rows

    for i, item in enumerate(data):
        y = (len(data) - i) * y_spacing

        min_val = item["min"]
        max_val = item["max"]
        q1, q3 = item["middle_50"]
        mean = item["mean"]

        # --- Plot whisker line ---
        ax.hlines(y, min_val, max_val, color='black', linewidth=2)

        # --- Plot whisker caps ---
        cap_height = 0.15
        ax.vlines(min_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)
        ax.vlines(max_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)

        # --- Plot box (middle 50%) ---
        ax.barh(y, q3 - q1, left=q1, height=0.2, color='steelblue', alpha=0.7, edgecolor='none')

        # --- Plot mean dot ---
        ax.plot(mean, y, 'o',
                markersize=10,
                markerfacecolor='black',
                markeredgecolor='white',
                markeredgewidth=1.5)

        # --- Add All Raters and Benchmark text ---
        ax.text(5.2, y, f"{item['all_raters']:.1f}", va='center', ha='left', fontsize=11)
        ax.text(6.2, y, f"{item['benchmark']:.1f}", va='center', ha='left', fontsize=11)

    # --- Y-axis labels ---
    y_positions = [(len(data) - i) * y_spacing for i in range(len(data))]
    ax.set_yticks(y_positions)
    ax.set_yticklabels([item["competency"] for item in data], fontsize=12, weight='bold')

    # --- X-axis dynamic limits ---
    all_mins = [item["min"] for item in data]
    all_maxs = [item["max"] for item in data]

    x_min = min(all_mins) - 0.2
    data_max = max(all_maxs)

    # Reserve x_max for text columns (but this doesn't affect ticks)
    x_max = max(6.8, data_max)

    x_min_int = int(np.floor(x_min))
    x_max_int = int(np.ceil(x_max))

    ax.set_xlim(x_min, x_max)

    # Ticks only up to data max ceiling (not axis max)
    tick_max = int(np.ceil(data_max))
    ax.set_xlim(x_min, tick_max)

    custom_ticks = list(range(x_min_int, tick_max + 1))
    ax.set_xticks(custom_ticks)

    # Keep text at fixed positions beyond tick_max:
    all_raters_x = tick_max + 0.2
    benchmark_x = tick_max + 1.2

    # --- X-axis label ---
    # ax.set_xlabel("Score", fontsize=11)

    # --- Spine / border settings ---
    for spine in ['left', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)

    ax.spines['top'].set_visible(True)
    ax.spines['top'].set_position(('outward', 0))
    ax.spines['top'].set_linewidth(1)
    ax.spines['top'].set_color('black')

    # --- Tick settings ---
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=5, width=1, direction='out')
    ax.tick_params(axis='y', length=0)

    # --- Add headers for All Raters and Benchmark ---
    ax.text(5.2, max(y_positions) + y_spacing * 0.5, "All Raters", weight='bold', fontsize=12)
    ax.text(6.2, max(y_positions) + y_spacing * 0.5, "Benchmark", weight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig("reports/chart.png", dpi=300, bbox_inches='tight')
    plt.close()
    return "reports/chart.png"
    
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
x = 50
y = 780
c.setFont("Helvetica-Bold", 24)
c.setFillColor("darkgray")
sections = data['sections']
for section in sections:
    if section['header'] != 'Competency Rankings':
        break

    # Draw section header
    c.drawString(x, y, section['header'])

    # Draw line
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(2)
    c.line(50, y - 10, 550, y - 10)

    # Draw paragraph-style text
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.145, 0.145, 0.145)

    text = section['text'][0]  # Long paragraph string
    text_obj = c.beginText(x, y - 25)  # Start position below line
    text_obj.setLeading(14)  # Line spacing

    # Manually wrap text (simple logic)
    import textwrap
    wrapped_lines = textwrap.wrap(text, width=100)  # Adjust width as needed
    for line in wrapped_lines:
        text_obj.textLine(line)

    c.drawText(text_obj)

    chart_path = boxAndWhiskerChart(section['charts'][0]['data'])
    img_x = 150
    img_y = 300
    img_width = 300
    img_height = 400
    c.drawImage(chart_path, img_x, img_y, width=img_width, height=img_height)
    break  # Ensure only one section gets processed

c.showPage()
c.save()