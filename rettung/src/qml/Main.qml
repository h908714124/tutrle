import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import org.jbock.messagecontroller 1.0

Kirigami.ApplicationWindow {
    id: root

    title: "Simple Markdown viewer"

    minimumWidth: Kirigami.Units.gridUnit * 20
    minimumHeight: Kirigami.Units.gridUnit * 20
    width: minimumWidth
    height: minimumHeight

    pageStack.initialPage: initPage

    Component {
        id: initPage

        Kirigami.Page {
            title: "Markdown Viewer"

            MessageController {
                id: messagecontroller
                sourceText: sourceArea.text
            }

            ColumnLayout {
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                }
                Controls.TextArea {
                    id: sourceArea
                    placeholderText: "Write some Markdown code here"
                    wrapMode: Text.WrapAnywhere
                    Layout.fillWidth: true
                    Layout.minimumHeight: Kirigami.Units.gridUnit * 5 
                }

                RowLayout {
                    Layout.fillWidth: true

                    Controls.Button {
                        text: "Format"
                        onClicked: formattedText.text = messagecontroller.mdFormat()
                    }

                    Controls.Button {
                        text: "Clear"

                        onClicked: {
                            sourceArea.text = ""
                            formattedText.text = ""
                        }
                    }
                } 

                Text {
                    id: formattedText

                    textFormat: Text.RichText
                    wrapMode: Text.WordWrap

                    Layout.fillWidth: true
                    Layout.minimumHeight: Kirigami.Units.gridUnit * 5
                }
            }
    	}
    }
}

