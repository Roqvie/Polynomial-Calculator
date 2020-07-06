from PyQt5.QtWidgets import QApplication

import sys
import app


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = app.CalculatorUI()
    window.show()
    sys.exit(application.exec_())
