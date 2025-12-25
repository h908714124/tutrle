from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPlainTextEdit,
)
from tempfile import NamedTemporaryFile

import sys
import threading
import time
import signal
import subprocess

BANNER = """
Tool to add a luks2 passphrase
"""

STYLE_MESSAGE="font-weight: bold; color: white; font-family: monospace"

def get_device(label):
    result = subprocess.run(["blkid", "--label", label], capture_output=True, text=True)
    return result.stdout.rstrip()

def check_pw(string):
    pwfile = NamedTemporaryFile().name
    with open(pwfile, "w") as outfile:
        outfile.write(string)
    with open(pwfile, "r") as infile:
        result = subprocess.run(["pwscore"], stdin=infile, capture_output=True, text=True)
        if result.returncode != 0:
            return result.stderr.rstrip()
    return None

def set_password(device, pw):
    pwfile = NamedTemporaryFile().name
    with open(pwfile, "w") as outfile:
        outfile.write(pw)
    result = subprocess.run(
                ["sudo", "cryptsetup", "luksOpen", "-q", "--disable-external-tokens", "--key-file", pwfile, "--test-passphrase", device],
                capture_output=True, text=True)
    if result.returncode == 0:
        return {"success": f"{device}: passphrase exists", "again": "yes"}
    result = subprocess.run(
                ["sudo", "cryptsetup", "luksAddKey", "--token-type", "systemd-tpm2", device, pwfile],
                capture_output=True, text=True)
    if result.returncode == 0:
        return {"success": f"{device}: OK"}
    else:
        return {"failure": result.stderr.rstrip()}

class MainDialog(QDialog):

    def set_passwords(self, pw):
        self.label_message.setPlainText("")
        success = True
        again = 0
        for label in ["linuxhome", "linuxroot"]:
            result = set_password(get_device(label), pw)
            if "again" in result:
                again += 1
            if "success" in result:
                self.signal_append_message.emit(result["success"])
            else:
                success = False
                self.signal_append_message.emit("error: " + result["failure"])
        if again == 2:
            self.signal_append_message.emit("The passphrase was already set.")
            self.signal_append_message.emit("You may close this window now.")
            self.signal_enter_final_state.emit()
        elif success:
            self.signal_append_message.emit("The passphrase was saved.")
            self.signal_append_message.emit("You may close this window now.")
            self.signal_enter_final_state.emit()
        else:
            self.signal_unfreeze.emit()

    def on_pb_ok_clicked(self, checked):
        if self.final_state:
            self.parent.close()
            return
        pw = self.et_pw.text()
        if pw != self.et_confirm.text():
            self.label_message.setPlainText("no match")
            return
        error = check_pw(pw)
        if error:
            self.label_message.setPlainText(error)
            return
        self.label_message.setPlainText("")
        self.freeze()
        threading.Thread(target = lambda : self.set_passwords(pw)).start()

    def reject(self):
        if self.running:
            pass
        else:
            self.parent.close()

    def enter_final_state(self):
        self.final_state = True
        self.pb_ok.setEnabled(True)
        self.pb_ok.setText("close window")
        self.pb_ok.setFocus()
        self.et_pw.setEnabled(False)
        self.et_confirm.setEnabled(False)
        self.label_message.setStyleSheet(STYLE_MESSAGE + "; background-color: #006400")
        QApplication.restoreOverrideCursor()

    def freeze(self):
        self.running = True
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.et_pw.setEnabled(False)
        self.et_confirm.setEnabled(False)
        self.pb_ok.setEnabled(False)

    def unfreeze(self):
        self.running = False
        self.pb_ok.setEnabled(True)
        self.et_confirm.setEnabled(True)
        self.et_pw.setEnabled(True)
        QApplication.restoreOverrideCursor()

    signal_enter_final_state = Signal()
    signal_append_message = Signal(str)
    signal_unfreeze = Signal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.running = False
        self.final_state = False
        box = QVBoxLayout(self)
        st_banner = QLabel(BANNER.rstrip())
        st_banner.setWordWrap(True)
        box.addWidget(st_banner)
        self.init_form(box)
        self.pb_ok = QPushButton("OK", self)
        self.pb_ok.setDefault(True)
        self.pb_ok.setEnabled(False)
        self.pb_ok.clicked.connect(self.on_pb_ok_clicked)
        self.label_message = QPlainTextEdit()
        self.label_message.setFixedHeight(100)
        self.label_message.setReadOnly(True)
        self.label_message.setStyleSheet(STYLE_MESSAGE)
        self.label_message.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.signal_append_message.connect(self.label_message.appendPlainText)
        self.signal_enter_final_state.connect(self.enter_final_state)
        self.signal_unfreeze.connect(self.unfreeze)
        box.addWidget(self.pb_ok)
        box.addWidget(self.label_message)

    def on_text_changed(self):
        pw = self.et_pw.text()
        confirm = self.et_confirm.text()
        self.pb_ok.setEnabled(len(pw) >= 8 and pw == confirm)

    def init_form(self, box):
        layout = QGridLayout()
        self.et_pw = QLineEdit()
        self.et_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.et_confirm = QLineEdit()
        self.et_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.et_pw.textChanged.connect(self.on_text_changed)
        self.et_confirm.textChanged.connect(self.on_text_changed)
        layout.addWidget(QLabel("passphrase:"), 0, 0)
        layout.addWidget(self.et_pw, 0, 1)
        layout.addWidget(QLabel("confirm:"), 1, 0)
        layout.addWidget(self.et_confirm, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        box.addWidget(widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("add luks2 passphrase")
        self.setFixedWidth(460)
        self.setCentralWidget(MainDialog(self))

signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
