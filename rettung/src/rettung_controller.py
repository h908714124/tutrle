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
import time
import subprocess

QML_IMPORT_NAME = "org.jbock.rettung.controller"
QML_IMPORT_MAJOR_VERSION = 1

def get_device(label):
    result = subprocess.run(["blkid", "--label", label], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.rstrip()

def dark_theme():
    return QCoreApplication.instance().styleHints().colorScheme() == Qt.ColorScheme.Dark

def create_info(message, again=False, error=False):
    return {
        "message": message,
        "type": "info",
        "again": "yes" if again else "no",
        "error": "yes" if error else "no",
    }

def create_error(message):
    return {"message": message, "type": "error", "again": "no"}

def create_success(message):
    return {"message": message, "type": "success", "again": "no"}

def check_pw(string):
    pwfile = NamedTemporaryFile().name
    with open(pwfile, "w") as outfile:
        outfile.write(string)
    with open(pwfile, "r") as infile:
        result = subprocess.run(["/usr/bin/pwscore"], stdin=infile, capture_output=True, text=True,
            env={"LANG": "de_DE.UTF-8"})
        if result.returncode != 0:
            return result.stderr.rstrip()
    return None

def crypt_setup(device, pw):
    pwfile = NamedTemporaryFile().name
    with open(pwfile, "w") as outfile:
        outfile.write(pw)
    result = subprocess.run(
                ["sudo", "cryptsetup", "luksOpen", "-q", "--disable-external-tokens", "--key-file", pwfile, "--test-passphrase", device],
                capture_output=True, text=True, env={"LANG": "de_DE.UTF-8"})
    if result.returncode == 0:
        return create_info(f"{device}: bereits vorhanden", again=True)
    result = subprocess.run(
                ["sudo", "cryptsetup", "luksAddKey", "--token-type", "systemd-tpm2", device, pwfile],
                capture_output=True, text=True, env={"LANG": "de_DE.UTF-8"})
    if result.returncode == 0:
        return create_info(f"{device}: OK")
    else:
        return create_info(result.stderr.rstrip(), error=True)

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
        self._messages = []

    def insert_message(self, message):
        self._messages.insert(0, message)
        self.signal_messages_changed.emit()

    def clear_messages(self):
        if len(self._messages) == 0:
            return
        self._messages.clear()
        self.signal_messages_changed.emit()

    def set_message(self, message):
        if len(self._messages) == 1 and self._messages[0] == message:
            return
        self._messages.clear()
        self._messages.append(message)
        self.signal_messages_changed.emit()

    def change_state(self, state):
        if self._state == state:
            return
        self._state = state
        self.signal_state_changed.emit()

    def set_password(self, pw):
        success = True
        again = 0
        for label in ["linuxhome", "linuxroot"]:
            device = get_device(label)
            if device is None:
                success = False
                self.insert_message(create_info(f"Kein device mit label \"{label}\""))
                time.sleep(1)
                continue
            result = crypt_setup(device, pw)
            if result["again"] == "yes":
                again += 1
            if result["error"] == "yes":
                success = False
            self.insert_message(result)
        time.sleep(1)
        if again == 2:
            self.insert_message(create_info("Sie können dieses Fenster nun schliessen."))
            self.insert_message(create_success("Rettungsschlüssel bereits vorhanden"))
            self.change_state("final")
        elif success:
            self.insert_message(create_info("Um den Rettungsschlüssel zu testen, können Sie versuchen, ihn erneut zu vergeben."))
            self.insert_message(create_info("Sie können dieses Fenster nun schliessen."))
            self.insert_message(create_success("Rettungsschlüssel gespeichert"))
            self.change_state("final")
        else:
            self.insert_message(create_error("Fehler"))
            self.update_lockstate(clear=False)
        QApplication.restoreOverrideCursor()

    @Slot()
    def onSubmit(self):
        if self._state == "final":
            QCoreApplication.instance().quit()
            return
        pw = self._pw
        if len(pw) < 8 or pw != self._confirm:
            self.insert_message(create_error("passphrase mismatch"))
            return
        error = check_pw(pw)
        if error:
            self.set_message(create_error(error))
            return
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.change_state("busy")
        self.clear_messages()
        threading.Thread(target = lambda : self.set_password(pw)).start()

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

    def is_match(self):
        return len(self._pw) >= 8 and self._pw == self._confirm

    @confirmField.setter
    def confirmField(self, val):
        self._confirm = val
        self.update_lockstate()

    def update_lockstate(self, clear=True):
        if self.is_match():
            error = check_pw(self._pw)
            if error:
                self.set_message(create_error(error))
                return
            else:
                if clear:
                    self.clear_messages()
                self.change_state("unlocked")
        elif len(self._pw) == 0 and len(self._confirm) == 0:
            if clear:
                self.clear_messages()
            self.change_state("locked")
        else:
            self.set_message(create_info("no match"))
            self.change_state("locked")
