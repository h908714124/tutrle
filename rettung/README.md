# Just run

```
make run
```

### Run again?

```
pipx run --system-site-packages --spec . rettung
```

### Read the docs!

* https://develop.kde.org/docs/getting-started/kirigami/setup-python/
* https://develop.kde.org/docs/getting-started/python/python-app/
* https://develop.kde.org/docs/getting-started/python/python-package/
* https://doc.qt.io/qt-6/qtqml-javascript-expressions.html
* https://doc.qt.io/qtforpython-6/examples/example_quick_window.html
* https://doc.qt.io/qt-6/qtqml-javascript-topic.html

### Read stackoverflow!

* https://stackoverflow.com/questions/71719614/address-text-element-on-qml/71720831

### Read source code!

* https://code.qt.io/qt/qtdeclarative.git
* https://code.qt.io/qt/qtbase.git
* https://codebrowser.dev/qt6/qtdeclarative/src/quickcontrols/material/qquickmaterialstyle.cpp.html

### Color picker!

* https://doc.qt.io/qt-6/qtquickcontrols-material.html

### Example: Finding source of qml TextField

```
ug -Fnr 'qmltype TextField' ../qtdeclarative/src/
```
