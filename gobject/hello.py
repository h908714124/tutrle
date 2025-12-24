import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        long_label = Gtk.Label(label="Here is a very long chunk of text.")
        self.set_child(long_label)

class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        GLib.set_application_name("My Gtk Application")

    def do_activate(self):
        win = MainWindow(application=app)
        win.set_title("Hello World")
        win.set_default_size(460, 320)
        win.show()

app = MyApplication()
app.run()
