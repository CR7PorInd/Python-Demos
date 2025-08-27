// UniversalComponentsDemo.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    width: 800
    height: 600

    Column {
        anchors.centerIn: parent
        spacing: 16

        Text {
            text: "Universal Components Demo"
            font.pixelSize: 24
        }

        Button {
            text: "Click Me"
        }

        CheckBox {
            text: "Enable feature"
        }

        Slider {
            from: 0; to: 100
            value: 50
        }

        ProgressBar {
            value: 0.6
        }

        TextField {
            placeholderText: "Enter text"
            width: 200
        }

        ComboBox {
            model: ["Option A", "Option B", "Option C"]
        }

        Switch {
            text: "Dark Mode"
        }

        SpinBox {
            from: 0; to: 10
        }

        RadioButton {
            text: "Choice 1"
        }
        RadioButton {
            text: "Choice 2"
        }

        MenuBar {
            Menu {
                title: "File"
                MenuItem { text: "Open" }
                MenuItem { text: "Save" }
                MenuSeparator { }
                MenuItem { text: "Exit" }
            }
        }
    }
}
