import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import org.jbock.rettung.controller 1.0

Kirigami.ApplicationWindow {
    id: root

    title: "add luks2 passphrase"

    width: Kirigami.Units.gridUnit * 20
    height: Kirigami.Units.gridUnit * 30

    pageStack.initialPage: Kirigami.ScrollablePage {
        id: mainPage
        title: "Tool to add a luks2 passphrase"

        RettungController {
            id: controller
            pwField: pwField.text
            confirmField: confirmField.text
        }

        ColumnLayout {

            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
            }

            TextEdit {
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                text: "You can set a new luks2 passphrase here. " + 
                    "If you already had this passphrase, the tool will do nothing and tell you about it."
            }

            GridLayout {
                columns: 2

                TextInput {
                    text: "passphrase:"
                }

                Controls.TextField {
                    id: pwField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    enabled: controller.state === "locked" || controller.state === "unlocked"
                    Keys.onReturnPressed: {
                        controller.onSubmit()
                    }
                }

                TextInput {
                    text: "confirm:"
                }

                Controls.TextField {
                    id: confirmField
                    Layout.fillWidth: true
                    echoMode: TextInput.Password
                    enabled: controller.state === "locked" || controller.state === "unlocked"
                    Keys.onReturnPressed: {
                        controller.onSubmit()
                    }
                }
            }

            Controls.Button {
                Layout.fillWidth: true
                text: "OK"
                onClicked: {
                    controller.onSubmit()
                }
                enabled: controller.state === "unlocked"
            }

            Repeater {

                model: controller.messages

                Controls.TextArea {
                    wrapMode: Text.WordWrap
                    width: parent.parent.parent.width
                    readOnly: true
                    text: modelData
                    Layout.fillWidth: true
                }
            }
        }
    }
}

