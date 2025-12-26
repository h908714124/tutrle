import sys
import signal

from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine

from rettung.rettung_controller import RettungController # noqa: F401

signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load(QUrl.fromLocalFile(Path(__file__).parent.joinpath("qml/Main.qml")))
app.exec()
