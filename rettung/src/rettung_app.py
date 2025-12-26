import os
import sys
import signal

from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl, qWarning
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlApplicationEngine

from rettung.rettung_controller import RettungController # noqa: F401

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Needed to close the app with Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    qml_file = Path(__file__).parent / "qml/Main.qml"
    engine.load(QUrl.fromLocalFile(qml_file))

    if len(engine.rootObjects()) == 0:
        qWarning("error: no root objects")
        quit()

    app.exec()

if __name__ == "__main__":
    main()
