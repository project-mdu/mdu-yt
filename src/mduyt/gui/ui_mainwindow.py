# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 730)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_5 = QGridLayout(self.groupBox_5)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.encoding_checkbox = QCheckBox(self.groupBox_5)
        self.encoding_checkbox.setObjectName(u"encoding_checkbox")

        self.gridLayout_5.addWidget(self.encoding_checkbox, 0, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.encoding_method_combo = QComboBox(self.groupBox_5)
        self.encoding_method_combo.setObjectName(u"encoding_method_combo")

        self.horizontalLayout_6.addWidget(self.encoding_method_combo)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.preset_combo = QComboBox(self.groupBox_5)
        self.preset_combo.setObjectName(u"preset_combo")

        self.horizontalLayout_7.addWidget(self.preset_combo)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.label_5)

        self.quality_spinbox = QSpinBox(self.groupBox_5)
        self.quality_spinbox.setObjectName(u"quality_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.quality_spinbox.sizePolicy().hasHeightForWidth())
        self.quality_spinbox.setSizePolicy(sizePolicy1)
        self.quality_spinbox.setMinimumSize(QSize(64, 0))

        self.horizontalLayout_8.addWidget(self.quality_spinbox)

        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_7 = QLabel(self.groupBox_5)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_10.addWidget(self.label_7)

        self.outputvideo_combo = QComboBox(self.groupBox_5)
        self.outputvideo_combo.setObjectName(u"outputvideo_combo")

        self.horizontalLayout_10.addWidget(self.outputvideo_combo)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)

        self.lossless_checkbox = QCheckBox(self.groupBox_5)
        self.lossless_checkbox.setObjectName(u"lossless_checkbox")

        self.horizontalLayout_12.addWidget(self.lossless_checkbox)


        self.gridLayout_5.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_5, 3, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.history_view = QWidget(self.centralwidget)
        self.history_view.setObjectName(u"history_view")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.history_view.sizePolicy().hasHeightForWidth())
        self.history_view.setSizePolicy(sizePolicy2)
        self.history_view.setMinimumSize(QSize(0, 341))

        self.verticalLayout_5.addWidget(self.history_view)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.clear_history_button = QPushButton(self.centralwidget)
        self.clear_history_button.setObjectName(u"clear_history_button")

        self.horizontalLayout_14.addWidget(self.clear_history_button)

        self.showlog_button = QPushButton(self.centralwidget)
        self.showlog_button.setObjectName(u"showlog_button")

        self.horizontalLayout_14.addWidget(self.showlog_button)


        self.verticalLayout_5.addLayout(self.horizontalLayout_14)


        self.gridLayout_6.addLayout(self.verticalLayout_5, 5, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.status_label = QLabel(self.centralwidget)
        self.status_label.setObjectName(u"status_label")
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setMinimumSize(QSize(221, 0))

        self.horizontalLayout_13.addWidget(self.status_label)

        self.horizontalSpacer = QSpacerItem(298, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer)

        self.playlist_progress_label = QLabel(self.centralwidget)
        self.playlist_progress_label.setObjectName(u"playlist_progress_label")
        sizePolicy.setHeightForWidth(self.playlist_progress_label.sizePolicy().hasHeightForWidth())
        self.playlist_progress_label.setSizePolicy(sizePolicy)
        self.playlist_progress_label.setMinimumSize(QSize(201, 0))
        self.playlist_progress_label.setLayoutDirection(Qt.LeftToRight)
        self.playlist_progress_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.playlist_progress_label)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout_4.addWidget(self.progress_bar)


        self.gridLayout_6.addLayout(self.verticalLayout_4, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.url_input = QLineEdit(self.centralwidget)
        self.url_input.setObjectName(u"url_input")

        self.horizontalLayout_2.addWidget(self.url_input)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.download_button = QPushButton(self.centralwidget)
        self.download_button.setObjectName(u"download_button")

        self.horizontalLayout.addWidget(self.download_button)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")

        self.horizontalLayout.addWidget(self.stop_button)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout_6.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.video_radio = QRadioButton(self.groupBox)
        self.video_radio.setObjectName(u"video_radio")

        self.verticalLayout.addWidget(self.video_radio)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.resolution_combo = QComboBox(self.groupBox_2)
        self.resolution_combo.setObjectName(u"resolution_combo")

        self.horizontalLayout_3.addWidget(self.resolution_combo)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.fps_checkbox = QCheckBox(self.groupBox_2)
        self.fps_checkbox.setObjectName(u"fps_checkbox")

        self.horizontalLayout_4.addWidget(self.fps_checkbox)

        self.fps_combo = QComboBox(self.groupBox_2)
        self.fps_combo.setObjectName(u"fps_combo")

        self.horizontalLayout_4.addWidget(self.fps_combo)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.audio_radio = QRadioButton(self.groupBox)
        self.audio_radio.setObjectName(u"audio_radio")

        self.verticalLayout_2.addWidget(self.audio_radio)

        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.format_combo = QComboBox(self.groupBox_3)
        self.format_combo.setObjectName(u"format_combo")

        self.horizontalLayout_5.addWidget(self.format_combo)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_3)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_3 = QGridLayout(self.groupBox_4)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.thumbnail_checkbox = QCheckBox(self.groupBox_4)
        self.thumbnail_checkbox.setObjectName(u"thumbnail_checkbox")

        self.verticalLayout_3.addWidget(self.thumbnail_checkbox)

        self.metadata_checkbox = QCheckBox(self.groupBox_4)
        self.metadata_checkbox.setObjectName(u"metadata_checkbox")

        self.verticalLayout_3.addWidget(self.metadata_checkbox)

        self.playlist_checkbox = QCheckBox(self.groupBox_4)
        self.playlist_checkbox.setObjectName(u"playlist_checkbox")

        self.verticalLayout_3.addWidget(self.playlist_checkbox)


        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_4, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.folder_path = QLineEdit(self.groupBox_6)
        self.folder_path.setObjectName(u"folder_path")

        self.horizontalLayout_15.addWidget(self.folder_path)

        self.folder_button = QPushButton(self.groupBox_6)
        self.folder_button.setObjectName(u"folder_button")
        sizePolicy1.setHeightForWidth(self.folder_button.sizePolicy().hasHeightForWidth())
        self.folder_button.setSizePolicy(sizePolicy1)

        self.horizontalLayout_15.addWidget(self.folder_button)


        self.gridLayout_7.addLayout(self.horizontalLayout_15, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_6, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"YouTube Downloader", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Advanced", None))
        self.encoding_checkbox.setText(QCoreApplication.translate("MainWindow", u"Custom Encoding", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Encoder:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Preset:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Bitrate:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Kbps", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Output format:", None))
        self.lossless_checkbox.setText(QCoreApplication.translate("MainWindow", u"Lossless Encoding", None))
        self.clear_history_button.setText(QCoreApplication.translate("MainWindow", u"Clear history", None))
        self.showlog_button.setText(QCoreApplication.translate("MainWindow", u"Show log", None))
        self.status_label.setText("")
        self.playlist_progress_label.setText("")
        self.download_button.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Download Options", None))
        self.video_radio.setText(QCoreApplication.translate("MainWindow", u"Video + Audio", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Video Options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Resolution:", None))
        self.fps_checkbox.setText(QCoreApplication.translate("MainWindow", u"FPS:", None))
        self.audio_radio.setText(QCoreApplication.translate("MainWindow", u"Audio only", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Audio Options", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Extra", None))
        self.thumbnail_checkbox.setText(QCoreApplication.translate("MainWindow", u"Embed Thumbnails", None))
        self.metadata_checkbox.setText(QCoreApplication.translate("MainWindow", u"Embed Metadata", None))
        self.playlist_checkbox.setText(QCoreApplication.translate("MainWindow", u"Download as Playlists", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Download directory location", None))
        self.folder_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
    # retranslateUi

