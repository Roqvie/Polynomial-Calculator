from PyQt5 import (QtWidgets, QtSvg)
from PyQt5.QtGui import (QIcon, QPixmap)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIntValidator, QValidator

from io import BytesIO
import matplotlib.pyplot as plot

from design import Ui_MainWindow


class CalculatorUI(QtWidgets.QMainWindow, Ui_MainWindow):
    # Constants for field
    P, N = 2, 3
    calc_buffer = []


    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pValidator = QIntValidator(2,9)
        self.nValidator = QIntValidator(3,128)

        self.generate_buttons(self.PrPolynomialElemGrid, first=True)

        self.p.setValidator(self.pValidator)
        self.n.setValidator(self.nValidator)

        """self.p.setValidator(self.pValidator)
        self.n.setValidator(self.nValidator)"""

        # Connect buttons with events
        self.p \
            .textChanged \
            .connect(
                lambda: self.generate_buttons(self.PrPolynomialElemGrid)
            )
        self.n \
            .textChanged \
            .connect(
                lambda: self.generate_buttons(self.PrPolynomialElemGrid)
            )
        self.append \
            .clicked \
            .connect(
                self._plus
            )
        self.undo \
            .clicked \
            .connect(
                self._undo
            )


    def generate_buttons(self, grid, first=False):
        """Generate buttons and puts it in grid"""

        self._clear_grid(grid)

        # Check parameters
        if not first:
            sender = self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(),0)[0]
            if state != QValidator.Acceptable:
                sender.setStyleSheet('background-color: #F6989D;\n')
                p, n = 2, 3
            else:
                sender.setStyleSheet('background-color: #EEEEEC;\n')
                p, n = int(self.p.text()), int(self.n.text())
        else:
            p, n = self.P, self.N

        # Generate buttons
        self._create_grid(p, n, 8, grid)


    def _clear_grid(self, grid):
        """Clears grid from buttons"""

        if grid.count():
            for i in range(grid.count()):
                grid.itemAt(i).widget().close()


    def _create_grid(self, p, n, cols, grid):
        """Put generated buttons in grid"""

        for i in range(n+1):
            # Generate button with TeX string: 'x^{i}'
            button = self._generate_button(i, 'x')
            grid.addWidget(button, i//cols, i%cols, 1, 1)
            button.clicked.connect(self._add)


    def _generate_button(self, power, base):
        """Generate button with svg-icon from TeX string"""

        tex_string = self._create_tex_string(power, base)
        pixmap = QPixmap()
        pixmap.loadFromData(self._render_tex(tex_string))
        pushButton = CustomPushButton(
            pixmap=pixmap,
            power=power,
            base=base,
            tex=self._create_tex_string(power, base)
        )
        return pushButton


    def _create_tex_string(self, power, base):
        """Generate TeX-based string from parameters"""

        if power == 0:
            return r'$1$'
        elif power == 1:
            return r'$%s$' % base
        else:
            return r'$%s^{%s}$' % (base, power)


    def _render_tex(self, tex_string, format='svg', fontsize=16):
        """Render TeX string to svg-file"""

        # Create figure
        plot.rc('mathtext', fontset='cm')
        figure = plot.figure(figsize=(0.01, 0.01))
        figure.text(0, 0, tex_string, fontsize=fontsize, color='black')
        # Save rendered figure in bytes
        output = BytesIO()
        figure.savefig(output, format=format, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.02)
        plot.close(fig=figure)
        output.seek(0)

        return output.read()


    def _render_input(self):
        """Render last TeX string from calc_buffer"""

        pixmap = QPixmap()
        if len(self.calc_buffer):
            pixmap.loadFromData(self._render_tex(self.calc_buffer[-1][0], fontsize=18))
            self.label.setPixmap(pixmap)
        else:
            pixmap.loadFromData(self._render_tex('', fontsize=18))
            self.label.setPixmap(pixmap)


    def _add(self):
        """Add element in input"""

        sender = self.sender()
        if len(self.calc_buffer):
            self.calc_buffer.append([self.calc_buffer[-1][0] + sender.tex, sender.power])
        else:
            self.calc_buffer.append([sender.tex, sender.power])

        self._render_input()


    def _plus(self):
        if len(self.calc_buffer):
            self.calc_buffer.append([self.calc_buffer[-1][0] + " + ", 'plus'])
            self._render_input()


    def _undo(self):
        if len(self.calc_buffer):
            self.calc_buffer.pop()
            self._render_input()


class CustomPushButton(QtWidgets.QPushButton):
    """Custom class for some fields"""

    def __init__(self, pixmap, power, base, tex):
        super().__init__()
        self.power = power
        self.base = base
        self.tex = tex
        self.setIcon(QIcon(pixmap))
