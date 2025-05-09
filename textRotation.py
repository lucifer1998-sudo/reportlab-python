from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

class VerticalText(Flowable):
    def __init__(self, text, width=60, height=60, font_name="Helvetica-Bold", font_size=10):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height
        self.font_name = font_name
        self.font_size = font_size

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFont(self.font_name, self.font_size)

        text_width = stringWidth(self.text, self.font_name, self.font_size)

        
        self.canv.translate(self.width / 2, self.height / 2)

        
        self.canv.rotate(90)
        self.canv.drawCentredString(0, -text_width / 2, self.text)

        self.canv.restoreState()
