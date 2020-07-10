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
from PyQt5.QtCore import QSize, Qt



from design import Ui_MainWindow
from table import Ui_Table
from utils import _render_tex, _create_tex_string, get_field


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
        self.generate_field \
            .clicked \
            .connect(
                self.show_field
            )

    def show_field(self):
        """Show new window with table"""

        rows = int(self.p.text()) ** int(self.n.text())
        polynomial = self.calc_buffer[-1][1]
        self.table = CustomTable(rows,3,3,polynomial)
        self.table.show()


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

        tex_string = _create_tex_string(power, base)
        pixmap = QPixmap()
        pixmap.loadFromData(_render_tex(r'$'+tex_string+r'$'))
        pushButton = CustomPushButton(
            pixmap=pixmap,
            power=power,
            base=base,
            tex=_create_tex_string(power, base)
        )
        return pushButton


    def _render_input(self):
        """Render last TeX string from calc_buffer"""

        pixmap = QPixmap()
        if len(self.calc_buffer):
            pixmap.loadFromData(_render_tex(r'$'+self.calc_buffer[-1][0]+r'$', fontsize=18))
            self.label.setPixmap(pixmap)
        else:
            pixmap.loadFromData(_render_tex('', fontsize=18))
            self.label.setPixmap(pixmap)


    def _add(self):
        """Add element in input"""

        sender = self.sender()
        if len(self.calc_buffer):
            old_item = list(self.calc_buffer[-1][1])
            old_item.append(sender.power)
            new_item = [
                self.calc_buffer[-1][0] + sender.tex,
                old_item
            ]
            self.calc_buffer.append(new_item)
        else:
            self.calc_buffer.append([sender.tex, [sender.power]])

        self._render_input()


    def _plus(self):
        if len(self.calc_buffer):
            self.calc_buffer.append([
                self.calc_buffer[-1][0] + r" + ",
                self.calc_buffer[-1][1]
                ])
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


class CustomTable(QtWidgets.QMainWindow, Ui_Table):

    def __init__(self, rows, cols, n, polynomial):
        super().__init__()
        self.setupUi(self)

        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setHorizontalHeaderLabels(['Степень a','Многочлен', 'Вектор'])
        self.tableWidget.setIconSize(QSize(250,40))

        # Generate elements
        tex_strings = [r'$'+_create_tex_string(i,'a')+r'$' for i in range(rows)]
        for i, string in enumerate(tex_strings):
            item = QtWidgets.QTableWidgetItem()
            pixmap = QPixmap()
            pixmap.loadFromData(_render_tex(string))
            item.setIcon(QIcon(pixmap))
            self.tableWidget.setItem(i,0,item)

        field = get_field(n, polynomial)
        tex_strings = [[_create_tex_string(i, 'a') for i, bit in enumerate(elem) if bit == 1] for elem in field]
        tex_strings = ['+'.join(elem) for elem in tex_strings]
        tex_strings = [r'$'+elem+r'$' for elem in tex_strings]
        for i, string in enumerate(tex_strings):
            item = QtWidgets.QTableWidgetItem()
            pixmap = QPixmap()
            pixmap.loadFromData(_render_tex(string))
            item.setIcon(QIcon(pixmap))
            self.tableWidget.setItem(i,1,item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(field[i]))
            self.tableWidget.setItem(i,2,item)
