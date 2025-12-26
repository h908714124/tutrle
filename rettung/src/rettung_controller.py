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

import threading
import subprocess

QML_IMPORT_NAME = "org.jbock.rettung.controller"
QML_IMPORT_MAJOR_VERSION = 1

def dark_theme():
    return QCoreApplication.instance().styleHints().colorScheme() == Qt.ColorScheme.Dark

def color_info():
    return "#042f2e" if dark_theme() else "#99f6e4"

def color_error():
    return "#7c2d12" if dark_theme() else "#fca5a5"

def color_success():
    return "#14532d" if dark_theme() else "#86efac"

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
            {"message": "1 Hi there!" * 12, "bg": color_info()},
            {"message": "OUCH" * 3, "bg": color_error()},
            {"message": "yum" * 3, "bg": color_success()},
        ]

    def set_password(self, pw):
        subprocess.run(["sleep", "2"],
                capture_output=True, text=True)
        QApplication.restoreOverrideCursor()
        self._state = "unlocked"
        self._messages.insert(0, "OUCH")
        self.signal_messages_changed.emit()
        self.signal_state_changed.emit()

    def get_bab(self):
        return "bab " * 100

    @Slot()
    def onSubmit(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self._state = "busy"
        self.signal_state_changed.emit()
        threading.Thread(target = lambda : self.set_password(self.get_bab())).start()

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
            if self._state == "unlocked":
                return
            self._state = "unlocked"
            self.signal_state_changed.emit()
        else:
            if self._state == "locked":
                return
            self._state = "locked"
            self.signal_state_changed.emit()
