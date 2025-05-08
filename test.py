from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import navy, black, white, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
import textwrap

import matplotlib.pyplot as plt

# ---- Your JSON data (simplified version here, use your full JSON in real case) ----

import json
# Sample data

def plotBarChart(items) :
    
    # text_values = [item['text'] for item in items if item.get('type') == 'bar']
    # bar_data_flat = [item['data'][0] for item in items if item.get('type') == 'bar' and item['data']]
    # print(bar_data_flat)
    # exit('done')

    labels = []
    values = []
    flag = False
    for item in items:
        if item.get('type') == 'bar':
            flag = True
            labels.append(item['text'])
            if item['data']:
                values.append(item['data'][0])
            else:
                values.append(0)

    if not flag : 
        return False

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color='skyblue')

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.set_xticklabels([])
    max_height = max(values)
    ax.set_ylim(0, max_height)

    label_y = max_height

    for bar, category in zip(bars, labels):
        ax.annotate(category,
                    xy=(bar.get_x() + bar.get_width() / 2, label_y),
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    chart_path = "reports/barchart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    return chart_path

with open("data/sample.json") as f:
    chart_json = json.load(f)

chart_data = chart_json["sections"][1]['charts']

    

# ---------------------------------------------------
# PDF setup
# ---------------------------------------------------
page_width, page_height = A4
c = canvas.Canvas("grid_chart_example.pdf", pagesize=A4)


yAxis = 780

for chart in chart_data :
    totalCols = chart['cols']
    for rowIndex , row in enumerate(chart['rows']) : 
        colspan = row.get('colspan')

        flagChartCreated = False
        xAxis = 50
        yAxis = yAxis - 10

        if(rowIndex > 1 ) : 
            xAxis += 10

        for colIndex, col in enumerate(row['cols']) : # this is one row
            
            text = col["text"]
            if (colspan == totalCols) :
                c.setFillColor("royalblue")
                c.setStrokeColor("royalblue")
                c.rect(xAxis, 780, xAxis + 400, 25, fill=1)
                c.setFont("Helvetica-Bold", 8)
                c.setFillColor("white")
                indent = 2
                c.drawString(52 + indent, 790, text)
            else : 
                if(col.get('type') != 'bar' and col.get('rowspan') != '*') : 

                    if(colIndex != 0) :
                        xAxis = xAxis + 28
                    # draw the column 
                    c.setFillColor("black")
                    c.setFont("Helvetica", 8)
                    c.setLineWidth(1.5)
                    
                    wrap_width = 50


                    wrapped_lines = textwrap.wrap(text, width=wrap_width)
                    for line in wrapped_lines:
                        c.drawString(xAxis, yAxis, line)
                        if(len(wrapped_lines) > 1) :
                            print(text)
                            yAxis -= 10
                        
                    if(colIndex == 0) :
                        xAxis = xAxis + 250
                        


                if(flagChartCreated) : 
                    continue
                
                barChart = plotBarChart(row['cols'])

                if(barChart) :
                    flagChartCreated = True

                    img_x = 150
                    img_y = 300
                    img_width = 200
                    img_height = 100
                    c.drawImage(barChart, xAxis, yAxis - 35, width=img_width, height=img_height)
                    yAxis -= 35
c.showPage()
c.save()

print("PDF saved as grid_chart_example.pdf")
