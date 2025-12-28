import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import org.kde.kirigami as Kirigami
import org.jbock.rettung.controller

Kirigami.ApplicationWindow {
    id: root

    title: "add luks2 passphrase"

    width: Kirigami.Units.gridUnit * 20
    height: Kirigami.Units.gridUnit * 30

    pageStack.initialPage: Kirigami.ScrollablePage {
        id: mainPage
        title: "Rettung"

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
                        font.bold: modelData.type !== "info"
                        Layout.fillWidth: true
                        topPadding: 8
                        bottomPadding: 8
                        color: {
                            if (modelData.type === "info") {
                                palette.text
                            } else if (modelData.type === "error") {
                                palette.brightText
                            } else if (modelData.type === "success") {
                                palette.brightText
                            }
                        }
                        background: Rectangle {
                            border.width: modelData.type === "info" ? 1 : 0
                            border.color: palette.mid
                            radius: 6
                            color: {
                                if (modelData.type === "info") {
                                    palette.midlight
                                } else if (modelData.type === "error") {
                                    Material.accentColor
                                } else if (modelData.type === "success") {
                                    palette.highlight
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

