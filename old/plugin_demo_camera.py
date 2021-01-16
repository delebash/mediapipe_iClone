#!/usr/bin/env python3

# PyCharm
# import pydevd_pycharm
# pydevd_pycharm.settrace('127.0.0.1', port=12345, stdoutToServer=False,
#                         stderrToServer=False)
import cv2
import threading
import mediapipe as mp
import json
from google.protobuf.json_format import MessageToJson
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = None
cap = None

from mediapipe_iclone_converter import *

import RLPy
from PySide2.shiboken2 import wrapInstance
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import *
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
import BoneData
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
        self.initUI()

        self.Worker1 = Worker1()  # (optional) removed `.ui` because your thread should be an attr of the program, not of the ui. This is a matter of preference though.
        # self.Worker1.start()  # (optional) removed `.ui`
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)  # removed `.ui`

    def initUI(self):
        self.mocap_manager_dialog = RLPy.RUi.CreateRDialog()
        self.mocap_manager_dialog.SetWindowTitle("Mocap Manager")
        # -- Create Pyside layout for RDialog --#
        self.pyside_dialog = wrapInstance(int(self.mocap_manager_dialog.GetWindow()), QtWidgets.QDialog)
        self.pyside_dialog.setFixedWidth(600)
        self.pyside_dialog.setFixedHeight(600)
        self.mocap_layout = self.pyside_dialog.layout()

        # -- Add UI Elements --#
        self.info = QtWidgets.QLabel()
        # self.info.setFixedSize(1500, 800)
        # self.info.adjustSize()
        self.mocap_layout.addWidget(self.info)

        # self.connect_button = QtWidgets.QPushButton("Connect")
        # self.connect_button.clicked.connect(self.connect)
        # self.mocap_layout.addWidget(self.connect_button)

        self.info = QtWidgets.QLabel()
        # self.info.setFixedSize(500, 500)
        self.mocap_layout.addWidget(self.info)

        self.start_camera = QtWidgets.QPushButton("Start Camera")
        self.start_camera.clicked.connect(self.startCamera)
        self.mocap_layout.addWidget(self.start_camera)

        self.start_button = QtWidgets.QPushButton("Start Mocap")
        self.start_button.clicked.connect(self.start)
        self.mocap_layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton("Stop Mocap")
        self.stop_button.clicked.connect(self.stop)
        self.mocap_layout.addWidget(self.stop_button)


        return

    @Slot(QImage)  # (optional) decorator to indicate what object the signal will provide.
    def ImageUpdateSlot(self, Image):  # Unindented by 4 spaces.
        print('recieve frames')
        self.info.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):  # Unindented by 4 spaces.
        print('cancel feed')
        self.Worker1.stop()  # (optional) removed `.ui`
    #
    # # def connect(self):
    # #     self.obj.connectclient()

    # def startCamera(self):
    #     global hands
    #     global cap
    #     # For webcam input:
    #     hands = mp_hands.Hands(
    #         min_detection_confidence=0.5, min_tracking_confidence=0.5)
    #     cap = cv2.VideoCapture(0)
    #     while cap.isOpened():
    #         success, image = cap.read()
    #         if not success:
    #             print("Ignoring empty camera frame.")
    #             # If loading a video, use 'break' instead of 'continue'.
    #             continue
    #
    #         # Flip the image horizontally for a later selfie-view display, and convert
    #         # the BGR image to RGB.
    #         image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #         # To improve performance, optionally mark the image as not writeable to
    #         # pass by reference.
    #         image.flags.writeable = False
    #         results = hands.process(image)
    #         # if results.multi_hand_landmarks:
    #             # jsonStr = MessageToJson(results.multi_hand_landmarks[0])
    #             # jsonDict = json.loads(jsonStr)
    #             # new_pose = json2iclon(jsonDict)
    #             # pose_data = np.array([])
    #             # for array in new_pose:
    #             #     pose_data = np.concatenate([pose_data, array])
    #             # self.info.append(data)
    #             # self.proccessmocapdata(pose_data)
    #         # Draw the hand annotations on the image.
    #         image.flags.writeable = True
    #         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #         if results.multi_hand_landmarks:
    #             for hand_landmarks in results.multi_hand_landmarks:
    #                 mp_drawing.draw_landmarks(
    #                     image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    #         cv2.imshow('MediaPipe Hands', image)
    #         if cv2.waitKey(5) & 0xFF == 27:
    #             break
    #     hands.close()
    #     cap.release()

    def startCamera(self):
        self.Worker1.start()

    def start(self):
        self.startmocap()
        # self.startCamera()
        # t = threading.Thread(name='child procs', target=self.startCamera())
        # # t.setDaemon(True)
        # t.start()



    def stop(self):
        self.CancelFeed()
        mocap_manager.Stop()
        # global hand
        # global cap
        # # hands.close()
        # cap.release()
        # mocap_manager.Stop()

    def onMessage(self, msg):
        self.info.append(msg)

    def onData(self, data):
        new_pose = json2iclon(tpose, data)
        pose_data = np.array([])
        for array in new_pose:
            pose_data = np.concatenate([pose_data, array])
        # self.info.append(data)
        self.proccessmocapdata(pose_data)

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

        bone_list = BoneData.get_bone_list()
        hand_device.Initialize(bone_list)
        tpose = BoneData.get_t_pose()
        hand_device.SetTPoseData(avatar, tpose)

        if hand_device.IsTPoseReady(avatar) == True:
            mocap_manager.Start(RLPy.EMocapState_Preview)

    def process_data(self, frame_data):
        global hand_device
        global mocap_manager
        global avatar

        hand_device.ProcessData(0, frame_data, -1)

class Worker1(QThread):
    ImageUpdate = Signal(QImage)

    def run(self):
        # print('\nrun feed')
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                # print('send good frames')

    def stop(self):
        # print('stop feed')
        self.ThreadActive = False
        self.quit()
x = App()
x.show_dialog()
