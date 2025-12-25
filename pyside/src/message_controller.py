from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "org.jbock.messagecontroller"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class MessageController(QObject):

    sourceTextChanged = Signal()

    def __init__(self, _source_text=""):
        super().__init__()
        self._source_text = _source_text

    @Property(str, notify=sourceTextChanged)
    def sourceText(self):
        return self._source_text

    @sourceText.setter
    def sourceText(self, val):
        self._source_text = val
        self.sourceTextChanged.emit()

    @Slot(result=str)
    def mdFormat(self):
        return self._source_text
