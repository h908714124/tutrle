from PySide6.QtCore import (
    Qt,
    QObject,
    Signal,
    Slot,
    Property,
    QStringListModel,
    QCoreApplication,
)
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QApplication

from tempfile import NamedTemporaryFile

import threading
import subprocess

QML_IMPORT_NAME = "org.jbock.rettung.controller"
QML_IMPORT_MAJOR_VERSION = 1

def dark_theme():
    return QCoreApplication.instance().styleHints().colorScheme() == Qt.ColorScheme.Dark

def create_info(message):
    return {"message": message, "type": "info"}

def create_error(message):
    return {"message": message, "type": "error"}

def create_success(message):
    return {"message": message, "type": "success"}

def check_pw(string):
    pwfile = NamedTemporaryFile().name
    with open(pwfile, "w") as outfile:
        outfile.write(string)
    with open(pwfile, "r") as infile:
        result = subprocess.run(["/usr/bin/pwscore"], stdin=infile, capture_output=True, text=True,
            env={"LANG":"de_DE.UTF-8"})
        if result.returncode != 0:
            return result.stderr.rstrip()
    return None

@QmlElement
class RettungController(QObject):

    signal_state_changed = Signal()
    signal_text_changed = Signal()
    signal_messages_changed = Signal()

    def __init__(self):
        super().__init__()
        self._text = ""
        self._confirm = ""
        self._pw = ""
        self._state = "locked"
        self._messages = [
            create_info("1 Hi there!" * 12),
            create_error("OUCH"),
            create_success("yum " * 3),
        ]

    def insert_message(self, message):
        self._messages.insert(0, message)
        self.signal_messages_changed.emit()

    def clear_messages(self):
        self._messages.clear()
        self.signal_messages_changed.emit()

    def change_state(self, state):
        if self._state == state:
            return
        self._state = state
        self.signal_state_changed.emit()

    def set_password(self):
        error = check_pw(self._pw)
        if error:
            self.change_state("unlocked")
            self.insert_message(create_error(error))
            return
        subprocess.run(["sleep", "2"])
        QApplication.restoreOverrideCursor()
        self.change_state("final")
        self.insert_message(create_success("OK " * 3))

    @Slot()
    def onSubmit(self):
        if self._state == "final":
            QCoreApplication.instance().quit()
            return
        if len(self._pw) < 8 or self._pw != self._confirm:
            self.change_state("locked")
            self.insert_message(create_error("passphrase mismatch"))
            return
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.change_state("busy")
        self.clear_messages()
        threading.Thread(target = lambda : self.set_password()).start()

    @Property(str, notify=signal_text_changed)
    def messageText(self):
        return self._text

    @Property(str, notify=signal_state_changed)
    def state(self):
        return self._state

    @Property(str)
    def pwField(self):
        return self._pw

    @pwField.setter
    def pwField(self, val):
        self._pw = val
        self.update_lockstate()

    @Property(list, notify=signal_messages_changed)
    def messages(self):
        return self._messages

    @Property(str)
    def confirmField(self):
        return self._confirm

    @confirmField.setter
    def confirmField(self, val):
        self._confirm = val
        self.update_lockstate()

    def update_lockstate(self):
        if len(self._pw) >= 8 and self._pw == self._confirm:
            self.change_state("unlocked")
        else:
            self.change_state("locked")
