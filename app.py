from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from design import MainWindowUI
from utils import generate_button


class CalculatorUI(QtWidgets.QMainWindow, MainWindowUI):
    # Constants for field
    P, N = 2, 3
    PR_BUTTONS = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.p.editingFinished.connect(self.set_input_buttons)
        self.n.editingFinished.connect(self.set_input_buttons)


    def set_input_buttons(self):
        """Generate buttons for field with (p,n) parameters"""

        # Delete all buttons from layout
        if self.PrElementsGrid.count():
            for i in range(self.PrElementsGrid.count()):
                self.PrElementsGrid.itemAt(i).widget().close()

        # Set parameters
        given_p, given_n = int(self.p.text()), int(self.n.text())
        p = given_p if given_p else self.P
        n = given_n if given_n else self.N

        self._create_grid(p, n, 8, self.PrElementsGrid)


    def _create_grid(self, p, n, cols, grid):
        for i in range(n+1):
            grid.addWidget(generate_button(i, 'x'), i//cols, i%cols, 1, 1)
