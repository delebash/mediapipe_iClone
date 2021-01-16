#!/usr/bin/env python3

# PyCharm
import pydevd_pycharm
# pydevd_pycharm.settrace('127.0.0.1', port=12345, stdoutToServer=False,
#                         stderrToServer=False)
import cv2
import sys
import threading
import itertools
import mediapipe as mp
from mediapipe_iclone_converter import *
from google.protobuf.json_format import MessageToDict
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

from mediapipe_iclone_converter import *

import RLPy
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication

from PySide2.shiboken2 import wrapInstance
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import *
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtCore import QObject, Signal, Slot
import iClone_BoneData
from PySide2 import QtCore, QtGui, QtWidgets
# from iclone_json import  *

mocap_manager = RLPy.RGlobal.GetMocapManager()
avatar = None
hand_device_ID = "HandDevice"
hand_device = mocap_manager.AddHandDevice(hand_device_ID)
new_pose = None
use_right_hand = False

class App:
    """GUI Application using PySide2 widgets"""

    def __init__(self):
        # self.capturing = False
        # self.c = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.initUI()
        self.Worker1 = Worker1()  # (optional) removed `.ui` because your thread should be an attr of the program, not of the ui. This is a matter of preference though.
        # self.Worker1.start()  # (optional) removed `.ui`
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)  # removed `.ui


    def initUI(self):
        self.mocap_manager_dialog = RLPy.RUi.CreateRDialog()
        self.mocap_manager_dialog.SetWindowTitle("Mocap Manager")
        # -- Create Pyside layout for RDialog --#
        self.pyside_dialog = wrapInstance(int(self.mocap_manager_dialog.GetWindow()), QtWidgets.QDialog)
        self.pyside_dialog.setFixedWidth(600)
        self.pyside_dialog.setFixedHeight(600)
        self.mocap_layout = self.pyside_dialog.layout()

        # -- Add UI Elements --#
        self.video_size = QSize(320, 240)
        self.image_label = QLabel()
        # self.image_label.setFixedSize(self.video_size)
        self.mocap_layout.addWidget(self.image_label)

        self.start_camera = QtWidgets.QPushButton("Start Camera")
        self.start_camera.clicked.connect(self.startCamera)
        self.mocap_layout.addWidget(self.start_camera)

        self.start_mocap_button = QtWidgets.QPushButton("Start Mocap")
        self.start_mocap_button.clicked.connect(self.startMocap)
        self.mocap_layout.addWidget(self.start_mocap_button)

        self.stop_mocap_button = QtWidgets.QPushButton("Stop Mocap")
        self.stop_mocap_button.clicked.connect(self.stopMocap)
        self.mocap_layout.addWidget(self.stop_mocap_button)

        return

    @Slot(QImage)  # (optional) decorator to indicate what object the signal will provide.
    def ImageUpdateSlot(self, Image):  # Unindented by 4 spaces.
        # print('recieve frames')
        self.image_label.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):  # Unindented by 4 spaces.
        print('cancel feed')
        self.Worker1.stop()  # (optional) removed `.ui

    def startCamera(self):
        self.Worker1.start()

    def startMocap(self):
        self.startmocap()


    def stopMocap(self):
        print("pressed Quit")
        self.CancelFeed()
        mocap_manager.Stop()
        # self.capturing = False
        # cap = self.c
        # cv2.destroyAllWindows()
        # cap.release()
        # mocap_manager.Stop()
        # self.mocap_manager_dialog.Close()


    def onMessage(self, msg):
        self.info.append(msg)

    def onData(self, data):
        new_pose = json2iclon(tpose, data)
        pose_data = np.array([])
        for array in new_pose:
            pose_data = np.concatenate([pose_data, array])

    def onStop(self, msg):
        self.info.append('I am Diconnected')

    def show_dialog(self):
        self.mocap_manager_dialog.Show()

    def startmocap(self):
        global hand_device
        global avatar

        if avatar:
            hand_device.RemoveAvatar(avatar)
            avatar = None

        selection_list = RLPy.RScene.GetSelectedObjects()
        if len(selection_list) > 0:
            for object in selection_list:  # find first avatar
                object_type = object.GetType()
                if object_type == RLPy.EObjectType_Avatar:
                    avatar = object

        if avatar is None:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Please click on an avatar")
            msgBox.exec()
            return

        if hand_device is not None:
            hand_device.AddAvatar(avatar)
            hand_device.SetEnable(avatar, True)
            hand_device.SetProcessDataIndex(avatar, 0)

        hand_setting = hand_device.GetHandSetting(avatar)

        hand_setting.SetRightHandJoin(RLPy.EHandJoin_Wrist)
        hand_setting.SetLeftHandJoin(RLPy.EHandJoin_Wrist)
        hand_setting.SetHandJoinType(RLPy.EHandJoinType_UseParentBone)
        if use_right_hand:
            hand_setting.SetRightHandDataSource(RLPy.EHandDataSource_RightHand)
            hand_setting.SetLeftHandDataSource(RLPy.EHandDataSource_RightHand)
        else:
            hand_setting.SetRightHandDataSource(RLPy.EHandDataSource_LeftHand)
            hand_setting.SetLeftHandDataSource(RLPy.EHandDataSource_LeftHand)
        hand_setting.SetActivePart(RLPy.EBodyActivePart_Hand_R | RLPy.EBodyActivePart_Finger_R |
                                   RLPy.EBodyActivePart_Hand_L | RLPy.EBodyActivePart_Finger_L)

        device_setting = hand_device.GetDeviceSetting()
        device_setting.SetMocapCoordinate(RLPy.ECoordinateAxis_Y, RLPy.ECoordinateAxes_Z,
                                          RLPy.ECoordinateSystem_RightHand)
        device_setting.SetCoordinateOffset(0, [0, 0, 0])

        position_setting = device_setting.GetPositionSetting()
        rotation_setting = device_setting.GetRotationSetting()
        rotation_setting.SetType(RLPy.ERotationType_Euler)
        rotation_setting.SetUnit(RLPy.ERotationUnit_Degrees)
        rotation_setting.SetEulerOrder(RLPy.EEulerOrder_ZXY)
        rotation_setting.SetCoordinateSpace(RLPy.ECoordinateSpace_Local)
        position_setting.SetUnit(RLPy.EPositionUnit_Centimeters)
        position_setting.SetCoordinateSpace(RLPy.ECoordinateSpace_Local)

        bone_list = iClone_BoneData.hik_bone_list
        hand_device.Initialize(bone_list)
        tpose = iClone_BoneData.tpose
        flattened_tpose = list(itertools.chain.from_iterable(tpose))
        hand_device.SetTPoseData(avatar, flattened_tpose)

        if hand_device.IsTPoseReady(avatar) == True:
            mocap_manager.Start(RLPy.EMocapState_Preview)

    def process_mocap_data(self, frame_data):
        global hand_device
        global mocap_manager
        global avatar

        hand_device.ProcessData(0, frame_data, -1)

class Worker1(QThread):
    ImageUpdate = Signal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        hands = mp_hands.Hands(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)

        while self.ThreadActive:
            ret, frame = Capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)

            frame.flags.writeable = False
            results = hands.process(frame)
            results.flags.writeable = True

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    land = MessageToDict(hand_landmarks)
                    new_pose = mocap_to_iclone(land)
                    pose_data = np.array([])
                    for array in new_pose:
                        pose_data = np.concatenate([pose_data, array])
                    App().process_mocap_data(pose_data)

                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                # Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                image = QImage(frame, frame.shape[1], frame.shape[0],
                               frame.strides[0], QImage.Format_RGB888)

                self.ImageUpdate.emit(image)
                # print('send good frames')
        # cv2.waitKey(5)
    def stop(self):
        # print('stop feed')
        self.ThreadActive = False
        self.quit()

x = App()
x.show_dialog()


