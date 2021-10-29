from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import UIDriver

# Driver to run the application
def runApplication():
    app = QApplication(sys.argv)
    win = QMainWindow()
    ui = UIDriver.UIDriver()
    ui.setupUI(win)
    ui.setPage("welcome")
    win.show()
    sys.exit(app.exec_())

runApplication()
