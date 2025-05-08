import matplotlib.pyplot as plt
import numpy as np
import textwrap
from reportlab.lib.colors import navy, black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4


def boxAndWhiskerChart(chart_data):
    data = chart_data['data']
    legend_labels = chart_data.get('legend', {}).get('text', ["Min", "Max", "Mean", "Middle 50%"])

    chart_width_in = 7.5  # Match PDF printable width
    chart_height_in = len(data) * 0.6 + 1.5  # Extra space for legend

    fig, ax = plt.subplots(figsize=(chart_width_in, chart_height_in))

    y_spacing = 1.5
    for i, item in enumerate(data):
        y = (len(data) - i) * y_spacing

        min_val = item["min"]
        max_val = item["max"]
        q1, q3 = item["middle_50"]
        mean = item["mean"]

        ax.hlines(y, min_val, max_val, color='black', linewidth=2)
        cap_height = 0.15
        ax.vlines(min_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)
        ax.vlines(max_val, y - cap_height / 2, y + cap_height / 2, color='black', linewidth=2)

        ax.barh(y, q3 - q1, left=q1, height=0.2, color='steelblue', alpha=0.7, edgecolor='none')

        ax.plot(mean, y, 'o',
                markersize=10,
                markerfacecolor='black',
                markeredgecolor='white',
                markeredgewidth=1.5)

    # Y labels
    y_positions = [(len(data) - i) * y_spacing for i in range(len(data))]
    ax.set_yticks(y_positions)
    ax.set_yticklabels([item["competency"] for item in data], fontsize=12, weight='bold')

    # X limits and ticks
    all_mins = [item["min"] for item in data]
    all_maxs = [item["max"] for item in data]

    x_min = min(all_mins) - 0.2
    data_max = max(all_maxs)

    tick_max = int(np.ceil(data_max))
    x_min_int = int(np.floor(x_min))

    ax.set_xlim(x_min, tick_max)
    custom_ticks = list(range(x_min_int, tick_max + 1))
    ax.set_xticks(custom_ticks)

    # All Raters and Benchmark text
    all_raters_x = tick_max + 0.2
    benchmark_x = tick_max + 1.2

    for i, item in enumerate(data):
        y = (len(data) - i) * y_spacing
        ax.text(all_raters_x, y, f"{item['all_raters']:.1f}", va='center', ha='left', fontsize=11)
        ax.text(benchmark_x, y, f"{item['benchmark']:.1f}", va='center', ha='left', fontsize=11)


    # Hide spines
    for spine in ['left', 'right', 'bottom']:
        ax.spines[spine].set_visible(False)

    ax.spines['top'].set_visible(True)
    ax.spines['top'].set_position(('outward', 0))
    ax.spines['top'].set_linewidth(1)
    ax.spines['top'].set_color('black')

    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=5, width=1, direction='out')
    ax.tick_params(axis='y', length=0)

    # All Raters & Benchmark headers
    header_y = max(y_positions) + y_spacing * 0.5
    ax.text(all_raters_x, header_y, "All Raters", weight='bold', fontsize=12)
    ax.text(benchmark_x, header_y, "Benchmark", weight='bold', fontsize=12)

    # --------------------------------
    # 🏷️ Add legend at the bottom
    # --------------------------------

    # Position below the last row
    legend_y = min(y_positions) - y_spacing * 1.5

    # Values for the illustration whisker
    legend_min = x_min_int + 0.5
    legend_max = tick_max - 0.5
    legend_q1 = legend_min + (legend_max - legend_min) * 0.25
    legend_q3 = legend_min + (legend_max - legend_min) * 0.75
    legend_mean = (legend_q1 + legend_q3) / 2

    # Whisker line
    ax.hlines(legend_y, legend_min, legend_max, color='black', linewidth=2)
    # Caps
    ax.vlines(legend_min, legend_y - 0.15, legend_y + 0.15, color='black', linewidth=2)
    ax.vlines(legend_max, legend_y - 0.15, legend_y + 0.15, color='black', linewidth=2)
    # Box
    ax.barh(legend_y, legend_q3 - legend_q1, left=legend_q1, height=0.2,
            color='steelblue', alpha=0.7, edgecolor='none')
    # Mean dot
    ax.plot(legend_mean, legend_y, 'o',
            markersize=10,
            markerfacecolor='black',
            markeredgecolor='white',
            markeredgewidth=1.5)

    # Legend labels from JSON
    ax.text(legend_min - 0.1, legend_y, legend_labels[0], ha='right', va='center', fontsize=11)  # Min
    ax.text(legend_max + 0.1, legend_y, legend_labels[1], ha='left', va='center', fontsize=11)   # Max
    ax.text(legend_mean, legend_y - 0.3, legend_labels[2], ha='center', va='top', fontsize=11)   # Mean
    ax.text((legend_q1 + legend_q3) / 2, legend_y + 0.3, legend_labels[3], ha='center', va='bottom', fontsize=11)  # Middle 50%

    # --------------------------------

    plt.tight_layout()
    chart_path = "reports/chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    return chart_path


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
        # Draw line
        c.setStrokeColor(navy)
        c.setLineWidth(2)
        yAxis = yAxis - 10
        c.line(50, yAxis, 550, yAxis)

    else : 

        # ---- Left header ----
        left_header = section['header']['text'][0]
        c.setFont("Helvetica-BoldOblique", 16)
        c.setFillColor(navy)
        c.drawString(x_left, y_top, left_header)

        # ---- Right header ----
        right_header = section['header']['text'][1]
        c.setFont("Helvetica-Oblique", 12)
        c.drawRightString(page_width - 100, y_top + 12, right_header)

        # ---- Measure left header width ----
        left_text_width = stringWidth(left_header, "Helvetica-BoldOblique", 16)

        # ---- Draw the small curved corner ----
        corner_radius = 6  # Tight small curve
        corner_x = x_left - corner_radius
        corner_y = y_top - 2

        c.setStrokeColor(navy)
        c.setLineWidth(1.5)


        # Quarter arc (tight corner now)
        c.arc(
            corner_x, 
            corner_y - corner_radius, 
            corner_x + 2 * corner_radius, 
            corner_y + corner_radius, 
            startAng=180, 
            extent=90
        )

        # ---- Draw the horizontal line ----
        line_start_x = x_left + left_text_width + 4  # Small gap after text
        baseline_y = y_top + 4  # Slightly lower for alignment

        c.line(line_start_x, baseline_y, page_width - 50, baseline_y)

    # ---- Paragraph text ----
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
 