# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowCursorControl.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from VoiceSettings import Ui_VoiceControlSettingsForm
from back.vm1 import VirtualMouse
from back.VoiceAssistant import VoiceControl
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon

import cv2
import qimage2ndarray



class Ui_CursorControlWindow(QtWidgets.QMainWindow):
    def setupUi(self, CursorControlWindow):
        CursorControlWindow.setObjectName("CursorControlWindow")
        CursorControlWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CursorControlWindow.sizePolicy().hasHeightForWidth())
        CursorControlWindow.setSizePolicy(sizePolicy)
        CursorControlWindow.setMinimumSize(QtCore.QSize(900, 600))
        CursorControlWindow.setMaximumSize(QtCore.QSize(900, 600))
        # CursorControlWindow.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.centralwidget = QtWidgets.QWidget(CursorControlWindow)
        # self.centralwidget.setStyleSheet("background-color: rgb(143, 143, 255);")
        # self.centralwidget.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.setWindowIcon(QIcon('tap.png'))    
        self.centralwidget.setObjectName("centralwidget")
        self.AccelerationSlider = QtWidgets.QSlider(self.centralwidget)
        self.AccelerationSlider.setGeometry(QtCore.QRect(670, 80, 160, 22))
        self.AccelerationSlider.setStatusTip("")
        self.AccelerationSlider.setMaximum(20)
        self.AccelerationSlider.setMinimum(2)
        self.AccelerationSlider.setSingleStep(1)
        self.AccelerationSlider.setProperty("value", 10)
        self.AccelerationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.AccelerationSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.AccelerationSlider.setTickInterval(1)
        self.AccelerationSlider.setObjectName("AccelerationSlider")
        self.graphicsView = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(5, 61, 640, 480))
        self.graphicsView.setStyleSheet("background-color: #B3F059")
        self.graphicsView.setObjectName("graphicsView")
        self.CameraControlCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.CameraControlCheckBox.setGeometry(QtCore.QRect(690, 330, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CameraControlCheckBox.setFont(font)
        self.CameraControlCheckBox.setObjectName("CameraControlCheckBox")
        self.VoiceControlCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.VoiceControlCheckBox.setGeometry(QtCore.QRect(690, 380, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.VoiceControlCheckBox.setFont(font)
        self.VoiceControlCheckBox.setObjectName("VoiceControlCheckBox")

        self.LandMarksControlCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.LandMarksControlCheckBox.setGeometry(QtCore.QRect(690, 280, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LandMarksControlCheckBox.setFont(font)
        self.LandMarksControlCheckBox.setObjectName("LandMarksControlCheckBox")

        self.VoiceSettingstoolButton = QtWidgets.QToolButton(self.centralwidget)
        self.VoiceSettingstoolButton.setGeometry(QtCore.QRect(690, 460, 145, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.VoiceSettingstoolButton.setFont(font)
        self.VoiceSettingstoolButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        # self.VoiceSettingstoolButton.setStyleSheet("background-color: rgb(85, 170, 255);border: none;border-radius: 10px;color: #FFF;")
        self.VoiceSettingstoolButton.setObjectName("VoiceSettingstoolButton")
        self.ResetSettingsPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResetSettingsPushButton.setGeometry(QtCore.QRect(690, 510, 145, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ResetSettingsPushButton.setFont(font)
        # self.ResetSettingsPushButton.setStyleSheet("background-color: rgb(85, 170, 255);border: none;border-radius: 10px;color: #FFF;")
        self.ResetSettingsPushButton.setObjectName("ResetSettingsPushButton")
        self.CameraChooseComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.CameraChooseComboBox.setGeometry(QtCore.QRect(5, 20, 640, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CameraChooseComboBox.setFont(font)
        # self.CameraChooseComboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CameraChooseComboBox.setEditable(False)
        self.CameraChooseComboBox.setObjectName("CameraChooseComboBox")
        self.motionSpeedSlider = QtWidgets.QSlider(self.centralwidget)
        self.motionSpeedSlider.setGeometry(QtCore.QRect(670, 170, 160, 22))
        self.motionSpeedSlider.setStatusTip("")
        self.motionSpeedSlider.setMinimum(10)
        self.motionSpeedSlider.setMaximum(20)
        self.motionSpeedSlider.setProperty("value", 1)
        self.motionSpeedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.motionSpeedSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.motionSpeedSlider.setTickInterval(1)
        self.motionSpeedSlider.setObjectName("motionSpeedSlider")
        self.AccelerationLabel = QtWidgets.QLabel(self.centralwidget)
        self.AccelerationLabel.setGeometry(QtCore.QRect(670, 50, 160, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.AccelerationLabel.setFont(font)
        self.AccelerationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AccelerationLabel.setObjectName("AccelerationLabel")
        self.MotionSpeedLabel = QtWidgets.QLabel(self.centralwidget)
        self.MotionSpeedLabel.setGeometry(QtCore.QRect(670, 140, 160, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MotionSpeedLabel.setFont(font)
        self.MotionSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MotionSpeedLabel.setObjectName("MotionSpeedLabel")
        CursorControlWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CursorControlWindow)
        QtCore.QMetaObject.connectSlotsByName(CursorControlWindow)

        self.VoiceSettingstoolButton.clicked.connect(self.show_VoiceSettings)

        ###########################################
        #items for CameraChooseComboBox

        if len(VirtualMouse.devices):
            self.CameraChooseComboBox.addItems(VirtualMouse.devices)
        else:
            self.CameraChooseComboBox.addItem("None")

        self.frame_timer = QtCore.QTimer()

        self.CameraControlCheckBox.stateChanged.connect(self.setup_camera)
        self.CameraChooseComboBox.currentIndexChanged.connect(self.Choose_camera)

        self.voice_control = VoiceControl(LeftCkick="левый", RightClick="правый", DoubleLeftClick="двойной", ScrollLeft="влево", ScrollRight="вправо",ScrollUp="вверх", ScrollDown="вниз", DragAndDrop="взять")
        self.UI_voicesettings = Ui_VoiceControlSettingsForm()
        # self.UI_voicesettings.mouse_action[list, 'mouse_action'].connect(self.update_voiceassistant)

        self.VoiceControlCheckBox.stateChanged.connect(self.voice_activated)

        self.AccelerationSlider.valueChanged.connect(self.change_acceleration)

        self.motionSpeedSlider.valueChanged.connect(self.change_motionspeed)

        self.ResetSettingsPushButton.clicked.connect(self.reset_settings)

        self.LandMarksControlCheckBox.stateChanged.connect(self.change_landmarks)

    def change_landmarks(self):
        VirtualMouse.drawing_landmarks = not VirtualMouse.drawing_landmarks

    def change_motionspeed(self, value):
        VirtualMouse.frameR = value * 10
        print(value)

    def change_acceleration(self, value):
        VirtualMouse.smoothening = value
        print(value)

    def voice_activated(self):
        if self.VoiceControlCheckBox.isChecked():

            self.voice_control.start = True
            self.voice = Thread(target=self.voice_control.Start)
            self.voice.setDaemon(True)
            self.voice.start()

        else:
            # self.voice_control.Microphone.stream = None
            self.voice_control.start = False
            # QThread.__init__(self)
            # self.voice_control.Start()
        

    def retranslateUi(self, CursorControlWindow):

        _translate = QtCore.QCoreApplication.translate
        CursorControlWindow.setWindowTitle(_translate("CursorControlWindow", "Cursor control"))
        self.CameraControlCheckBox.setText(_translate("CursorControlWindow", "Camera control"))
        self.VoiceControlCheckBox.setText(_translate("CursorControlWindow", "Voice control"))
        self.LandMarksControlCheckBox.setText(_translate("CursorControlWindow", "Drawing landmarks"))
        self.VoiceSettingstoolButton.setWhatsThis(_translate("CursorControlWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.VoiceSettingstoolButton.setText(_translate("CursorControlWindow", "Voice settings"))
        self.ResetSettingsPushButton.setText(_translate("CursorControlWindow", "Reset to default settings"))
        self.AccelerationLabel.setText(_translate("CursorControlWindow", "Acceleration"))
        self.MotionSpeedLabel.setText(_translate("CursorControlWindow", "Motion speed"))

    def show_VoiceSettings(self):

        self.voicesettings = QtWidgets.QMainWindow()
        self.voicesettings.setWindowIcon(QIcon('voice-control.png'))
        with open('stylesheet.qss', 'r') as f:
            self.voicesettings.setStyleSheet(f.read())
        self.UI_voicesettings.setupUi(self.voicesettings)

        if self.voice_control.LeftCkick:
            self.UI_voicesettings.LeftClickTextEdit.setText(self.voice_control.LeftCkick)

        if self.voice_control.RightClick:
            self.UI_voicesettings.RightClickTextEdit.setText(self.voice_control.RightClick)

        if self.voice_control.DoubleLeftClick:
            self.UI_voicesettings.DBLeftClickTextEdit.setText(self.voice_control.DoubleLeftClick)

        if self.voice_control.DragAndDrop:
            self.UI_voicesettings.DragAndDropTextEdit.setText(self.voice_control.DragAndDrop)

        if self.voice_control.ScrollDown:
            self.UI_voicesettings.ScrollDownTextEdit.setText(self.voice_control.ScrollDown)

        if self.voice_control.ScrollUp:
            self.UI_voicesettings.ScrollUpTextEdit.setText(self.voice_control.ScrollUp)

        if self.voice_control.ScrollLeft:
            self.UI_voicesettings.ScrollLeftTextEdit.setText(self.voice_control.ScrollLeft)

        if self.voice_control.ScrollRight:
            self.UI_voicesettings.ScrollRightTextEdit.setText(self.voice_control.ScrollRight)
        
        self.UI_voicesettings.MicrophoneChooseComboBox.currentTextChanged.connect(self.choose_micro)

        if self.voice_control.show_microphone() is not None :
            self.UI_voicesettings.MicrophoneChooseComboBox.setCurrentText(self.voice_control.show_microphone())

    
        self.UI_voicesettings.signal.connect(self.update_voiceassistant)
        self.voicesettings.show()

    def reset_settings(self):
        self.motionSpeedSlider.setProperty("value", 1)
        self.AccelerationSlider.setProperty("value", 10)
        self.CameraControlCheckBox.setChecked(False)
        self.VoiceControlCheckBox.setChecked(False)

    def choose_micro(self,index):
        self.voice_control.select_microphone(index)
    
    def update_voiceassistant(self, value:list) -> None:
        if value[0]:
            self.voice_control.LeftCkick = value[0]
        else:
            self.voice_control.LeftCkick = None
        if value[1]:
            self.voice_control.RightClick = value[1]
        else:
            self.voice_control.RightClick = None
        if value[2]:
            self.voice_control.DoubleLeftClick = value[2]
        else:
            self.voice_control.DoubleLeftClick = None
        if value[3]:
            self.voice_control.ScrollUp = value[3]
        else:
            self.voice_control.ScrollUp = None
        if value[4]:
            self.voice_control.ScrollDown = value[4]
        else:
            self.voice_control.ScrollDown = None
        if value[5]:
            self.voice_control.ScrollLeft = value[5]
        else:
            self.voice_control.ScrollLeft = None
        if value[6]:
            self.voice_control.ScrollRight = value[6]
        else:
            self.voice_control.ScrollRight = None
        if value[7]:
            self.voice_control.DragAndDrop = value[7]
        else:
            self.voice_control.DragAndDrop = None

        self.voicesettings.close()
        

    def setup_camera(self):
        if self.CameraControlCheckBox.isChecked():

            if not VirtualMouse.cap.isOpened():

                VirtualMouse.SetCamera(self.CameraChooseComboBox.currentIndex())

            self.frame_timer.timeout.connect(self.display_video_stream)



            self.frame_timer.start(3)

        else:

            self.frame_timer.stop()
            VirtualMouse.cap.release()
            self.graphicsView.clear()
    
    def Choose_camera(self, index):
        VirtualMouse.SetCamera(index)

    def display_video_stream(self):
        success,image = VirtualMouse.Show_image()

        if not success:
            return False

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(image)
        self.graphicsView.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    with open('stylesheet.qss', 'r') as f:
        app.setStyleSheet(f.read())
    app.setWindowIcon(QIcon('tap.png'))
    CursorControlWindow = QtWidgets.QMainWindow()
    ui = Ui_CursorControlWindow()
    ui.setupUi(CursorControlWindow)
    CursorControlWindow.show()
    sys.exit(app.exec_())