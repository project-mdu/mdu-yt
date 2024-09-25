import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import Qt.labs.platform as Platform

ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 600
    title: "YouTube Downloader"

    property string downloadPath: ""

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        RowLayout {
            TextField {
                id: urlInput
                Layout.fillWidth: true
                placeholderText: "Enter YouTube URL"
            }
            Button {
                text: "Download"
                onClicked: backend.start_download(urlInput.text, audioRadio.checked, formatCombo.currentText, resolutionCombo.currentText, fpsCombo.currentText, root.downloadPath)
            }
        }

        RowLayout {
            RadioButton {
                id: videoRadio
                text: "Video:"
                checked: true
            }
            ComboBox {
                id: resolutionCombo
                model: ["720", "1080", "1440", "2160", "best"]
                enabled: videoRadio.checked
            }
            CheckBox {
                id: fpsCheckbox
                text: "FPS:"
                enabled: videoRadio.checked
            }
            ComboBox {
                id: fpsCombo
                model: ["30", "60", "auto"]
                enabled: videoRadio.checked && fpsCheckbox.checked
            }
            RadioButton {
                id: audioRadio
                text: "Audio:"
            }
            ComboBox {
                id: formatCombo
                model: ["wav", "mp3", "m4a", "flac"]
                enabled: audioRadio.checked
            }
        }

        RowLayout {
            Label {
                text: "Download folder:"
            }
            TextField {
                id: folderPath
                Layout.fillWidth: true
                text: root.downloadPath
            }
            Button {
                text: "Browse"
                onClicked: folderDialog.open()
            }
        }

        ProgressBar {
            id: progressBar
            Layout.fillWidth: true
            from: 0
            to: 100
            value: 0
        }

        Label {
            id: statusLabel
            text: "Ready"
        }

        ListView {
            id: historyList
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: backend.historyModel
            delegate: ItemDelegate {
                width: parent.width
                contentItem: RowLayout {
                    Image {
                        source: model.icon
                        Layout.preferredWidth: 32
                        Layout.preferredHeight: 32
                    }
                    ColumnLayout {
                        Label {
                            text: model.filename
                            font.bold: true
                        }
                        Label {
                            text: model.path
                            color: "gray"
                        }
                    }
                    Item { Layout.fillWidth: true }
                    Button {
                        icon.source: "qrc:/folder.svg"
                        onClicked: backend.open_file_location(model.path, model.filename)
                    }
                }
            }
        }

        Button {
            text: "Clear History"
            onClicked: backend.clear_history()
        }
    }

    Platform.FolderDialog {
        id: folderDialog
        title: "Select Download Folder"
        folder: Platform.StandardPaths.writableLocation(Platform.StandardPaths.DownloadLocation)
        onAccepted: {
            root.downloadPath = backend.normalize_path(folder)
            folderPath.text = root.downloadPath
        }
    }

    Connections {
        target: backend
        function onUpdateProgress(progress, fileSize, downloadSpeed, eta) {
            progressBar.value = progress
            statusLabel.text = `Downloading: ${progress.toFixed(1)}% | Size: ${fileSize} | Speed: ${downloadSpeed} | ETA: ${eta}`
        }
        function onShowError(error) {
            statusLabel.text = `Error: ${error}`
        }
        function onDownloadFinished(filename, filePath, fileType) {
            statusLabel.text = "Download completed!"
        }
    }

    Component.onCompleted: {
        root.downloadPath = backend.default_download_path
    }
}