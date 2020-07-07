from PyQt5 import (QtWidgets, QtSvg)
from PyQt5.QtGui import (QIcon, QPixmap, QPainter)
from PyQt5.QtCore import QSize
from design import MainWindowUI
from utils import (generate_button, _render)


class CalculatorUI(QtWidgets.QMainWindow, MainWindowUI):
    # Constants for field
    P, N = 2, 3
    calc_buffer = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Generate buttons for standart (p,n) parameters
        self.generate_buttons(self.PrimitiveElementsGrid)
        self.p.editingFinished.connect(lambda: self.generate_buttons(self.PrimitiveElementsGrid))
        self.n.editingFinished.connect(lambda: self.generate_buttons(self.PrimitiveElementsGrid))
        self.append.clicked.connect(self._plus)


    def generate_buttons(self, grid):
        """Generate buttons for grid with (p,n) parameters"""

        # Delete all buttons from grid
        if grid.count():
            for i in range(grid.count()):
                grid.itemAt(i).widget().close()

        # Check parameters
        given_p, given_n = int(self.p.text()), int(self.n.text())
        p = given_p if given_p else self.P
        n = given_n if given_n else self.N

        # Generate buttons
        self.create_grid(p, n, 8, grid)


    def create_grid(self, p, n, cols, grid):
        """Put generated buttons in grid"""

        for i in range(n+1):
            # Generate button with TeX string: 'x^{i}'
            button = generate_button(i, 'x')
            grid.addWidget(button, i//cols, i%cols, 1, 1)
            button.clicked.connect(self._add)


    def _add(self):
        sender = self.sender()
        if len(self.calc_buffer):
            self.calc_buffer.append([self.calc_buffer[-1][0] + sender.tex, sender.power])
        else:
            self.calc_buffer.append([sender.tex, sender.power])

        pixmap = QPixmap()
        pixmap.loadFromData(_render(self.calc_buffer[-1][0]))
        self.lable.setPixmap(pixmap)

    def _plus(self):
        if len(self.calc_buffer):
            self.calc_buffer.append([self.calc_buffer[-1][0] + "+", None])
            pixmap = QPixmap()
            pixmap.loadFromData(_render(self.calc_buffer[-1][0]))
            self.lable.setPixmap(pixmap)
