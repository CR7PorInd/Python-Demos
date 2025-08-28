from PySide6.QtWidgets import QWidget, QGridLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibModule(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Football Stats Charts")

        gridLayout = QGridLayout(self)

        # ===== Pie Chart =====
        pieData = {
            "Real Madrid": 15,
            "AC Milan": 7,
            "Liverpool": 6,
            "Bayern Munich": 6,
            "Barcelona": 5
        }
        pieLabels = list(pieData.keys())
        pieValues = list(pieData.values())

        pieFig = Figure(figsize=(4, 3))
        pieCanvas = FigureCanvas(pieFig)
        pieAx = pieFig.add_subplot(111)
        pieAx.pie(pieValues, labels=pieLabels, autopct=lambda p: f"{int(p*sum(pieValues)/100)} UCLs", startangle=90)
        pieAx.axis("equal")  # Equal aspect ratio for perfect circle
        pieAx.set_title("Top 5 UCL Winning Teams")
        gridLayout.addWidget(pieCanvas, 0, 0)

        # ===== Bar Chart =====
        barData = {
            "C. Ronaldo": 936,
            "Messi": 875,
            "Suárez": 583,
            "Lewandowski": 672,
            "Benzema": 508,
        }
        barCategories = list(barData.keys())
        barValues = list(barData.values())
        barColors = ["#6200EE", "#03DAC6", "#BB86FC", "#FFB300", "#03A9F4"]

        barFig = Figure(figsize=(4, 3))
        barCanvas = FigureCanvas(barFig)
        barAx = barFig.add_subplot(111)
        bars = barAx.bar(barCategories, barValues, color=barColors)
        for bar in bars:
            height = bar.get_height()
            barAx.text(bar.get_x() + bar.get_width() / 2, height + 5,
                       f"{height}", ha="center", va="bottom")
        barAx.set_ylabel("Goals")
        barAx.set_title("Top 5 Active All-Time Goalscorers")
        gridLayout.addWidget(barCanvas, 0, 1)

        # ===== Line Chart =====
        lineData = {
            2009: 30,
            2010: 48,
            2011: 60,
            2012: 63,
            2013: 69,
            2014: 61,
            2015: 57,
            2016: 55,
            2017: 53,
            2018: 49,
            2019: 39
        }
        lineX = list(lineData.keys())
        lineY = list(lineData.values())

        lineFig = Figure(figsize=(8, 3))
        lineCanvas = FigureCanvas(lineFig)
        lineAx = lineFig.add_subplot(111)
        lineAx.plot(lineX, lineY, marker="o", linestyle="-", color="#6200EE")

        # Annotate each point
        for xi, yi in zip(lineX, lineY):
            lineAx.text(xi, yi + 1, f"{xi}: {yi}", ha="center", va="bottom")

        lineAx.set_xlabel("Year")
        lineAx.set_ylabel("Goals")
        lineAx.set_title("Cristiano Goals per Year")
        gridLayout.addWidget(lineCanvas, 1, 0, 1, 2)  # spans 2 columns