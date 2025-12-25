from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

import threading
import subprocess

QML_IMPORT_NAME = "org.jbock.rettung.controller"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class RettungController(QObject):

    source_text_changed = Signal(name="sourceTextChanged")

    def __init__(self):
        super().__init__()
        self._source_text = ""

    def set_password(self, pw):
        subprocess.run(["sleep", "2"],
                capture_output=True, text=True)
        self._source_text = pw
        self.source_text_changed.emit()

    @Slot()
    def synchro_start(self):
        threading.Thread(target = lambda : self.set_password("bab")).start()

    @Property(str, notify=source_text_changed)
    def sourceText(self):
        return self._source_text
