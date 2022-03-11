import matplotlib
import matplotlib.pyplot as plt
import pandas_ta as ta
import sys
import yfinance as yf

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, figure):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        static_canvas = FigureCanvas(figure)
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

if __name__ == "__main__":
    arguments = iter(sys.argv)
    next(arguments)
    ticker = next(arguments, 'BTC-USD')
    period = next(arguments, '1y')
    data = yf.Ticker(ticker).history(period=period)[['Close', 'Open', 'High', 'Volume']]
    macd = ta.macd(close = data['Close'], fast = 12, slow = 26, signal = 9, append = True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(f'MACD Analysis of #{ticker} in #{period}')
    ax.set_ylabel('Price ($)')
    ax.set_xlabel('Time')
    ax.plot(data['Close'], color = 'black', linewidth = 3)
    ax2 = ax.twinx()
    ax2.plot(macd)
    ax2.legend(['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'])
    fig.tight_layout()
    fig.show()
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication()
    app = ApplicationWindow(fig)
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
