from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
    Property,
    QStringListModel,
)
from PySide6.QtQml import QmlElement

import threading
import subprocess

QML_IMPORT_NAME = "org.jbock.rettung.controller"
QML_IMPORT_MAJOR_VERSION = 1

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
            "1 Hi there!", "AHAHA",
            "2 Hi there!", "AHAHA",
            "3 Hi there!", "AHAHA",
            "4 Hi there!", "AHAHA",
            "5 Hi there!", "AHAHA",
            "6 Hi there!", "AHAHA",
            "7 Hi there!", "AHAHA",
            "8 Hi there!", "AHAHA",
            "9 Hi there!", "AHAHA",
            "10 Hi there!", "AHAHA",
            "11 Hi there!", "AHAHA",
            "12 Hi there!", "AHAHA",
            "13 Hi there!", "AHAHA",
            "14 Hi there!", "AHAHA",
            "15 Hi there!", "AHAHA",
            "16 Hi there!", "AHAHA",
        ]

    def set_password(self, pw):
        subprocess.run(["sleep", "2"],
                capture_output=True, text=True)
        self._text = pw
        self.signal_text_changed.emit()

    def get_bab(self):
        return "bab " * 100

    @Slot()
    def onPbOkClicked(self):
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
