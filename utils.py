from PyQt5 import (QtWidgets, QtSvg)
from PyQt5.QtGui import (QIcon, QPixmap, QPainter)
from PyQt5.QtCore import QSize
from io import BytesIO
import matplotlib.pyplot as plot


class CustomPushButton(QtWidgets.QPushButton):
    """Custom class for some fields"""
    def __init__(self):
        super().__init__()
        self.power = None
        self.base = None
        self.tex = None


def generate_button(power, base):
    """Generate button with TeX svg-icon"""

    pixmap = QPixmap()
    pixmap.loadFromData(_render(tex_string=get_tex_string(power, base)))
    pushButton = CustomPushButton()
    pushButton.setIcon(QIcon(pixmap))
    pushButton.setIconSize(QSize(40,25))
    pushButton.power = power
    pushButton.base = base
    pushButton.tex = get_tex_string(power, base)
    return pushButton

def get_tex_string(power, base):
    """Generate TeX-based string from parameters"""
    if power == 0:
        return r'$1$'
    elif power == 1:
        return r'$%s$' % base
    else:
        return r'$%s^{%s}$' % (base, power)


def _render(tex_string, filename=None, format='png', fontsize=16, bytes=True):
    """Render TeX string to svg-file"""

    plot.rc('mathtext', fontset='cm')
    figure = plot.figure(figsize=(0.01, 0.01))
    figure.text(0, 0, tex_string, fontsize=fontsize, color='black')
    # Save rendered svg in bytes
    if bytes:
        output = BytesIO()
        figure.savefig(output, format=format, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0.02)
        plot.close(fig=figure)
        output.seek(0)
        return output.read()
    else:
        figure.savefig(filename, format=format, transparent=True, bbox_inches='tight', pad_inches=0.02)
        plot.close(fig=figure)
