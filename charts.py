from PySide6.QtWidgets import QGridLayout
from PySide6.QtCharts import QPieSeries, QBarSeries, QPieSlice, QBarSet, QChartView, QChart, QLineSeries, QCategoryAxis, \
    QValueAxis
from PySide6.QtCore import Qt, QEasingCurve, QMargins
from PySide6.QtWidgets import QWidget

pie_data = {
    "Real Madrid": 15,
    "AC Milan": 7,
    "Liverpool": 6,
    "Bayern Munich": 6,
    "Barcelona": 5
}

bar_data = {
    "Cristiano Ronaldo": 936,
    "Lionel Messi": 875,
    "Robert Lewandowski": 672,
    "Luis Suárez": 583,
    "Karim Benzema": 508
}

line_data = {
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






class ChartModule(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt Charts")

        self.grid = QGridLayout(self)
        self.setLayout(self.grid)

        # <editor-fold desc="Pie Chart">
        self.pieChart = QChart()
        self.pieChart.setTitle("UCL Top 5 Winning Clubs")
        self.pieChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.pieChart.setAnimationEasingCurve(QEasingCurve.Type.OutBounce)
        self.pieChart.createDefaultAxes()
        self.pieChart.legend().setVisible(True)
        self.pieChart.setMargins(QMargins(20, 20, 20, 20))
        self.pieChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.pieChartView = QChartView(self.pieChart)
        self.pieChartView.setRubberBand(QChartView.RubberBand.ClickThroughRubberBand)

        self.pie = QPieSeries()
        for key, value in pie_data.items():
            self.pie.append(QPieSlice(key, value))
        self.pie.setPieSize(0.4)
        self.pie.setLabelsVisible(True)
        self.pie.slices()[0].setBrush(Qt.GlobalColor.red)
        self.pie.slices()[1].setBrush(Qt.GlobalColor.magenta)
        self.pie.slices()[2].setBrush(Qt.GlobalColor.yellow)
        self.pie.slices()[3].setBrush(Qt.GlobalColor.green)
        self.pie.slices()[4].setBrush(Qt.GlobalColor.cyan)
        self.pieChart.addSeries(self.pie)
        # </editor-fold>

        # <editor-fold desc="Bar Chart">
        self.bar = QBarSeries()
        for key, value in bar_data.items():
            s = QBarSet(key)
            s.append(value)
            self.bar.append(s)
        self.bar.setBarWidth(0.4)
        self.bar.setLabelsVisible(True)
        self.bar.setLabelsPosition(QBarSeries.LabelsPosition.LabelsCenter)

        self.barChart = QChart()
        self.barChart.addSeries(self.bar)
        self.barChart.setTitle("All time top 5 goalscorers")
        self.barChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.barChart.setAnimationEasingCurve(QEasingCurve.Type.BezierSpline)
        self.barChart.createDefaultAxes()
        self.barChart.setMargins(QMargins(20, 20, 20, 20))
        self.barChart.legend().setVisible(True)
        self.barChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        baxisY = QValueAxis()
        baxisY.setRange(0, 1000)  # set min/max as needed
        baxisY.setTickCount(201)  # 11 ticks = integer values 0, 10, 20, ..., 100
        baxisY.setLabelFormat("%d")  # force integer display
        self.barChart.setAxisY(baxisY, self.bar)

        self.barChartView = QChartView(self.barChart)
        self.barChartView.setRubberBand(QChartView.RubberBand.ClickThroughRubberBand)
        # </editor-fold>

        # <editor-fold desc="Line Chart">
        self.line = QLineSeries()
        for key, value in line_data.items():
            self.line.append(key - 2009, value)
        self.line.setName("Cristiano Ronaldo - Goals 2010-2018")
        self.line.setPointsVisible(True)
        self.line.setPointLabelsVisible(True)
        self.line.setPointLabelsFormat("@yPoint")
        self.line.setPointLabelsClipping(True)
        self.line.setPointLabelsColor(Qt.GlobalColor.red)
        self.line.setColor(Qt.GlobalColor.darkBlue)

        self.lineChart = QChart()
        self.lineChart.addSeries(self.line)
        self.lineChart.setTitle("Cristiano Ronaldo Goals Per Year (2010-2018)")
        self.lineChart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self.lineChart.setAnimationEasingCurve(QEasingCurve.Type.InOutQuad)
        self.lineChart.createDefaultAxes()
        self.lineChart.legend().setVisible(False)
        self.lineChart.setMargins(QMargins(20, 20, 20, 20))

        laxisX = QCategoryAxis()
        laxisX.setTitleText("Year")
        for index, year in enumerate(list(line_data.keys())):
            laxisX.append(str(year), index + 0.5)  # label, position
        self.lineChart.setAxisX(laxisX, self.line)

        laxisY = QValueAxis()
        laxisY.setRange(0, 70)  # set min/max as needed
        laxisY.setTickCount(11)  # 11 ticks = integer values 0, 10, 20, ..., 100
        laxisY.setLabelFormat("%d")  # force integer display
        self.lineChart.setAxisY(laxisY, self.line)


        self.lineChartView = QChartView(self.lineChart)
        self.lineChartView.setRubberBand(QChartView.RubberBand.ClickThroughRubberBand)
        # </editor-fold>

        self.grid.addWidget(self.pieChartView, 0, 0)
        self.grid.addWidget(self.barChartView, 1, 0)
        self.grid.addWidget(self.lineChartView, 0, 1)
