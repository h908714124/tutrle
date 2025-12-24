import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

BANNER = """
Sie können einen neuen Rettungsschlüssel für Ihr Gerät vergeben.
Damit stellen Sie sicher, dass Sie Ihr Gerät immer entsperren können.
Der Rettungsschlüssel darf nicht zu einfach sein und muss
mindestens 8 Zeichen lang sein.
"""

class MainWindow(Gtk.ApplicationWindow):

    def on_key_press(self, keyval, keycode, state, user_data):
        if keycode == 65307:
            self.close()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        st_banner = Gtk.Label(label = BANNER.rstrip())
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(box)

        grid = Gtk.Grid()
        st_label1 = Gtk.Label(label = "Rettungsschlüssel")
        st_label2 = Gtk.Label(label = "Rettungsschlüssel wiederholen")
        st_banner = Gtk.Label(label = BANNER.rstrip())

        box.append(st_banner)
        box.append(st_label1)
        box.append(st_label2)

        keycont = Gtk.EventControllerKey()
        keycont.connect("key-pressed", self.on_key_press)
        self.add_controller(keycont)

class GridWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title="Grid Example")

        grid = Gtk.Grid()
        st_label1 = Gtk.Label(label = "Rettungsschlüssel")
        st_label2 = Gtk.Label(label = "Rettungsschlüssel wiederholen")
        st_banner = Gtk.Label(label = BANNER.rstrip())

        grid.attach(st_label1, 0, 0, 0, 0)
        grid.attach(st_label2, 0, 0, 1, 1)
        self.set_child(grid)

class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        GLib.set_application_name("My Gtk Application")

    def do_activate(self):
        win = MainWindow(application=app)
        win.set_title("Hello World")
        win.set_default_size(460, -1)
        win.set_visible(True)

app = MyApplication()
app.run()
