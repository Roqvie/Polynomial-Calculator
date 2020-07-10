from PyQt5 import (
                    QtWidgets,
                    QtSvg,
                    )
from PyQt5.QtGui import (
                            QIcon,
                            QPixmap,
                            QIntValidator,
                            QValidator,
                        )
from PyQt5.QtCore import (
                            QSize,
                            Qt,
                        )

from design import Ui_MainWindow
from table import Ui_Table
from utils import *


class CalculatorUI(QtWidgets.QMainWindow, Ui_MainWindow):
    # Constants for field
    P, N = 2, 3
    calc_buffer = []
    out_buffer = []


    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pValidator = QIntValidator(2,9)
        self.nValidator = QIntValidator(3,128)

        self.generate_buttons(self.PrPolynomialElemGrid, first=True, base='x', func=self._add)

        self.p.setValidator(self.pValidator)
        self.n.setValidator(self.nValidator)


        self.add.setEnabled(False)
        self.back.setEnabled(False)
        self.clean.setEnabled(False)
        self.multiply.setEnabled(False)
        self.calculate.setEnabled(False)


        # Connect buttons with events
        self.p \
            .textChanged \
            .connect(
                lambda: self.generate_buttons(self.PrPolynomialElemGrid, base='x', func=self._add)
            )
        self.n \
            .textChanged \
            .connect(
                lambda: self.generate_buttons(self.PrPolynomialElemGrid, base='x', func=self._add)
            )
        self.append \
            .clicked \
            .connect(
                self._plus_in
            )
        self.undo \
            .clicked \
            .connect(
                self._undo
            )
        self.generate_field \
            .clicked \
            .connect(
                self.show_field
            )
        self.generate_field \
            .clicked \
            .connect(
                lambda: self.generate_buttons(self.elementsGrid, base='a', validate=False, func=self._append)
            )
        self.generate_field \
            .clicked \
            .connect(
                self._enable
            )
        self.add \
            .clicked \
            .connect(
                self._plus_out
            )
        self.back \
            .clicked \
            .connect(
                self._back
            )
        self.clear \
            .clicked \
            .connect(
                self._clear
            )
        self.clean \
            .clicked \
            .connect(
                self._clean
            )


    def show_field(self):
        """Show new window with table"""

        rows = int(self.p.text()) ** int(self.n.text())
        polynomial = self.calc_buffer[-1][1]
        self.table = CustomTable(rows,3,polynomial)
        # Generate items
        tex_strings = [r'$'+create_tex_string(i,'a')+r'$' for i in range(rows)]
        self.table.generate_elements(tex_strings,0)
        tex_strings = self.table.generate_from_field(get_field(int(self.n.text()), polynomial))
        self.table.generate_elements(tex_strings,1)
        self.table.generate_elements(get_field(int(self.n.text()), polynomial), 2)
        self.table.show()


    def generate_buttons(self, grid, base, func, first=False, validate=True):
        """Generate buttons and puts it in grid"""

        self._clear_grid(grid)

        # Check parameters
        if not first and validate:
            sender= self.sender()
            validator = sender.validator()
            state = validator.validate(sender.text(),0)[0]
            if state != QValidator.Acceptable:
                sender.setStyleSheet('background-color: #F6989D;\n')
                p, n = 2, 3
            else:
                sender.setStyleSheet('background-color: #EEEEEC;\n')
                p, n = int(self.p.text()), int(self.n.text())
        elif validate:
            p, n = self.P, self.N
        elif not validate:
            p, n = int(self.p.text()), int(self.n.text())
        # Generate buttons
        self._create_grid(p, n, 8, grid, base, func)


    def render_input(self):
        """Render last TeX string from calc_buffer"""
        pixmap = QPixmap()
        if len(self.calc_buffer) and self.calc_buffer[-1][0] != '':
            string = r'$'+self.calc_buffer[-1][0]+r'$'
            pixmap.loadFromData(render_tex(string, fontsize=18))
        elif len(self.calc_buffer) == 0:
            pixmap.loadFromData(render_tex(''))
        elif self.calc_buffer[-1][0] == '':
            pixmap.loadFromData(render_tex(''))
        self.input_label.setPixmap(pixmap)


    def render_output(self):
        pixmap = QPixmap()
        if len(self.out_buffer) and self.out_buffer[-1][0] != '':
            pixmap.loadFromData(render_tex(r'$'+self.out_buffer[-1][0]+r'$', fontsize=18))
        elif len(self.out_buffer) == 0:
            pixmap.loadFromData(render_tex(''))
        elif self.out_buffer[-1][0] == '':
            pixmap.loadFromData(render_tex(''))
        self.output_label.setPixmap(pixmap)


    def _clear_grid(self, grid):
        """Clears grid from buttons"""

        if grid.count():
            for i in range(grid.count()):
                grid.itemAt(i).widget().close()


    def _create_grid(self, p, n, cols, grid, base, func):
        """Put generated buttons in grid"""

        for i in range(n+1):
            # Generate button with TeX string: 'x^{i}'
            button = self._generate_button(i, base)
            grid.addWidget(button, i//cols, i%cols, 1, 1)
            button.clicked.connect(func)


    def _generate_button(self, power, base):
        """Generate button with svg-icon from TeX string"""

        tex_string = create_tex_string(power, base)
        pixmap = QPixmap()
        pixmap.loadFromData(render_tex(r'$'+tex_string+r'$'))
        pushButton = CustomPushButton(
            pixmap=pixmap,
            power=power,
            base=base,
            tex=create_tex_string(power, base)
        )
        return pushButton


    def _add(self):
        """Add element in input"""

        sender = self.sender()
        if len(self.calc_buffer) and self.calc_buffer[-1][0] != '':
            old_item = list(self.calc_buffer[-1][1])
            old_item.append(sender.power)
            new_item = [
                self.calc_buffer[-1][0] + sender.tex,
                old_item
            ]
            self.calc_buffer.append(new_item)
        elif len(self.calc_buffer) == 0:
            self.calc_buffer.append([sender.tex, [sender.power]])
        elif self.calc_buffer[-1][0] == '':
            self.calc_buffer[-1] = [sender.tex, [sender.power]]

        self.render_input()


    def _plus_in(self):
        if len(self.calc_buffer):
            self.calc_buffer.append([
                self.calc_buffer[-1][0] + r' + ',
                self.calc_buffer[-1][1]
                ])
        self.render_input()


    def _undo(self):
        if len(self.calc_buffer):
            self.calc_buffer.pop()
        self.render_input()


    def _plus_out(self):
        if len(self.out_buffer):
            self.out_buffer.append([
                self.out_buffer[-1][0] + r' + ',
                self.out_buffer[-1][1]
                ])
        self.render_output()


    def _append(self):
        """Add element in input"""

        sender = self.sender()
        if len(self.out_buffer) and self.out_buffer[-1][0] != '':
            old_item = list(self.out_buffer[-1][1])
            old_item.append(sender.power)
            new_item = [
                self.out_buffer[-1][0] + sender.tex,
                old_item
            ]
            self.out_buffer.append(new_item)
        elif len(self.out_buffer) == 0:
            self.out_buffer.append([sender.tex, [sender.power]])
        elif self.out_buffer[-1][0] == '':
            self.out_buffer[-1] = [sender.tex, [sender.power]]

        self.render_output()


    def _back(self):
        if len(self.out_buffer):
            self.out_buffer.pop()
        self.render_output()


    def _clear(self):
        self.calc_buffer.append(['', None])
        self.render_input()


    def _clean(self):
        self.out_buffer.append(['', None])
        self.render_output()


    def _enable(self):
        self.add.setEnabled(True)
        self.back.setEnabled(True)
        self.clean.setEnabled(True)
        self.multiply.setEnabled(True)
        self.calculate.setEnabled(True)

class CustomPushButton(QtWidgets.QPushButton):
    """Custom class for some fields"""

    def __init__(self, pixmap, power, base, tex):
        super().__init__()
        self.power = power
        self.base = base
        self.tex = tex
        self.setIcon(QIcon(pixmap))


class CustomTable(QtWidgets.QMainWindow, Ui_Table):

    def __init__(self, rows, cols, polynomial):
        super().__init__()
        self.setupUi(self)

        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setHorizontalHeaderLabels(['Степень','Многочлен', 'Вектор'])
        self.tableWidget.setIconSize(QSize(250,40))


    def generate_elements(self,tex_strings: list, column: int):
        """Generate elements"""

        for i, string in enumerate(tex_strings):
            item = QtWidgets.QTableWidgetItem()
            pixmap = QPixmap()
            pixmap.loadFromData(render_tex(string))
            item.setIcon(QIcon(pixmap))
            self.tableWidget.setItem(i,column,item)


    def generate_from_field(self, field: list):
        """Generate tex_string from field"""

        tex_strings = [[create_tex_string(i, 'x') for i, bit in enumerate(elem) if bit == 1] for elem in field]
        tex_strings = ['+'.join(elem) for elem in tex_strings]
        tex_strings = [r'$'+elem+r'$' for elem in tex_strings]

        return tex_strings
