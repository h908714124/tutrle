import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import QtQuick.Controls.Universal
import org.kde.kirigami as Kirigami
import org.jbock.rettung.controller

Kirigami.ApplicationWindow {
    id: root

    title: "add luks2 passphrase"

    width: Kirigami.Units.gridUnit * 20
    height: Kirigami.Units.gridUnit * 30

    property bool darkMode: Application.styleHints.colorScheme === Qt.ColorScheme.Dark

    function borderShade() {
        return Application.styleHints.colorScheme === Qt.ColorScheme.Dark ? Material.Shade600 : Material.Shade400
    }
    function bgShade() {
        return Application.styleHints.colorScheme === Qt.ColorScheme.Dark ? Material.Shade800 : Material.Shade100
    }

    pageStack.initialPage: Kirigami.ScrollablePage {
        id: mainPage
        title: "Tool to add a luks2 passphrase"

        RettungController {
            id: controller
            pwField: pwField.text
            confirmField: confirmField.text
        }

        ColumnLayout {

            spacing: 16

            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
            }

            QQC2.Label {
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
                text: "You can set a new luks2 passphrase here. " + 
                    "If you already had this passphrase, the tool will do nothing and tell you about it."
            }

            GridLayout {
                columns: 2

                QQC2.Label {
                    text: "passphrase:"
                }

                QQC2.TextField {
                    id: pwField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    enabled: controller.state === "locked" || controller.state === "unlocked"
                    Keys.onReturnPressed: {
                        controller.onSubmit()
                    }
                }

                QQC2.Label {
                    text: "confirm:"
                }

                QQC2.TextField {
                    id: confirmField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    enabled: controller.state === "locked" || controller.state === "unlocked"
                    Keys.onReturnPressed: {
                        controller.onSubmit()
                    }
                }
            }

            QQC2.Button {
                Layout.fillWidth: true
                text: controller.state === "final" ? "Close" : "OK"
                onClicked: {
                    controller.onSubmit()
                }
                enabled: controller.state === "unlocked" || controller.state === "final"
            }

            ColumnLayout {
                Repeater {

                    model: controller.messages

                    QQC2.TextArea {
                        wrapMode: Text.WordWrap
                        width: parent.parent.parent.width
                        readOnly: true
                        text: modelData.message
                        Layout.fillWidth: true
                        topPadding: 8
                        bottomPadding: 8
                        background: Rectangle {
                            border.width: 2
                            border.color: Universal.chromeDisabledLowColor
                            radius: 6
                            color: {
                                if (modelData.type === "info") {
                                    return Material.backgroundColor
                                } else if (modelData.type === "error") {
                                    return Material.color(Material.Red, bgShade())
                                } else if (modelData.type === "success") {
                                    return Material.color(Material.Green, bgShade())
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

