from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit

import sys
import threading
import time

class MainWindow(QMainWindow):

    def set_password(self):
        time.sleep(2)
        self.pb_ok.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def on_pk_ok_clicked(self, checked):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.pb_ok.setEnabled(False)
        threading.Thread(target=self.set_password).start()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        layout = QVBoxLayout()
        le_pw = QLineEdit()
        le_confirm = QLineEdit()
        self.pb_ok = QPushButton("Press me!")
        self.pb_ok.clicked.connect(self.on_pk_ok_clicked)
        layout.addWidget(le_pw)
        layout.addWidget(le_confirm)
        layout.addWidget(self.pb_ok)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
