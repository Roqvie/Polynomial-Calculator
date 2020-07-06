from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from io import BytesIO
import matplotlib.pyplot as plot


class CustomPushButton(QtWidgets.QPushButton):
    """Custom class for some fields"""
    def __init__(self):
        super().__init__()
        self.power = None
        self.base = None


def generate_button(power, base):
    """Generate button with TeX svg-icon"""

    pixmap = QPixmap()
    pixmap.loadFromData(_render(power, base))
    pushButton = CustomPushButton()
    pushButton.setIcon(QIcon(pixmap))
    pushButton.setIconSize(QSize(40,28))
    pushButton.power = power
    pushButton.base = base
    return pushButton


def _render(power, base, format='svg', fontsize=16):
    """Render TeX string to svg"""

    tex_string = r'$%s^{%s}$' % (base,power)
    plot.rc('mathtext', fontset='cm')
    figure = plot.figure(figsize=(0.01, 0.01))
    figure.text(0, 0, tex_string, fontsize=fontsize, color='black')
    # Save rendered svg in bytes
    output = BytesIO()
    figure.savefig(output, format=format, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.02)
    plot.close(fig=figure)
    output.seek(0)
    return output.read()
