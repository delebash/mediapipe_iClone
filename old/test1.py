import RLPy

mocap_manager = RLPy.RGlobal.GetMocapManager()

avatar_list = RLPy.RScene.GetAvatars()
avatar = avatar_list[0]

facial_device_ID = "FacialDevice"
facial_device = mocap_manager.AddFacialDevice(facial_device_ID)

facial_setting = RLPy.RFacialSetting()
facial_setting.SetBlend(False)
facial_device.AddAvatar(avatar)
facial_device.SetFacialSetting(avatar, facial_setting)

facial_device.Initialize()

head_data1 = [0.3, 0.4, 0.5]
left_eye_data1 = [0.4, 0.5]
right_eye_data1 = [0.4, 0.5]
bone_data1 = [0.3, 0.4, 0.5, 0.3, 0.4, 0.4, 0.3, 0.4, 0.5, 0.3, 0.4, 0.4]
morph_data1 = [0] * 60
custom_data1 = [0] * 24

head_data2 = [0.3, 0.4, 0.5]
left_eye_data2 = [0.4, 0.5]
right_eye_data2 = [0.4, 0.5]
bone_data2 = [2.3, 2.4, 2.5, 2.3, 2.4, 2.4, 2.3, 2.4, 2.5, 2.3, 2.4, 2.4]
morph_data2 = [0.5] * 60
custom_data2 = [0] * 24

head_data3 = [0.3, 0.4, 0.5]
left_eye_data3 = [0.4, 0.5]
right_eye_data3 = [0.4, 0.5]
bone_data3 = [0.3, 0.4, 0.5, 0.3, 0.4, 0.4, 0.3, 0.4, 0.5, 0.3, 0.4, 0.4]
morph_data3 = [0.7] * 60
custom_data3 = [0] * 24

mocap_manager.Start(RLPy.EMocapState_Record)
facial_device.ProcessData(avatar, head_data1, left_eye_data1, right_eye_data1, morph_data1, custom_data1, bone_data1,frame1_time)
facial_device.ProcessData(avatar, head_data2, left_eye_data2, right_eye_data2, morph_data2, custom_data2, bone_data2,frame2_time)
facial_device.ProcessData(avatar, head_data3, left_eye_data3, right_eye_data3, morph_data3, custom_data3, bone_data3,frame3_time)
mocap_manager.Stop()
