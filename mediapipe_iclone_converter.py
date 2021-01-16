'''
generate new pose from left hand mocap data
'''
import numpy as np
import iClone_BoneData
import pytweening
# import vector3d.vector as Vect3d
import win32api
import win32con
from time import sleep

# tpose
def get_vecs(mocap_data):
    '''
    generate vetors
    :param mocap_data:
    :return:
    '''
    num = len(mocap_data)
    vects = []
    for i in range(num -1):
        # p1 = Vect3d.Point(mocap_data[i]['x'], mocap_data[i]['y'])
        # p2 = Vect3d.Point(mocap_data[i + 1]['x'], mocap_data[i + 1]['y'])
        pre_pt = np.array([mocap_data[i]['x'], mocap_data[i]['y'], mocap_data[i]['z']])
        next_pt = np.array([mocap_data[i + 1]['x'], mocap_data[i + 1]['y'],  mocap_data[i + 1]['z']])
        vec = np.array(next_pt) - np.array(pre_pt)
        vec = vec / np.linalg.norm(vec)
        # vec = Vect3d.from_points(p1,p2)
        vects.append(vec)
    return vects

def rot_angle(v1,v2):
    '''
    roation angle
    :param v1:
    :param v2:
    :return:
    '''
    theta = np.rad2deg(np.arccos(np.dot(v1,v2)))
    return theta
def get_pose(vects):
    '''
    generate new pose from vectors
    :param vects:
    :return:
    '''
    num = len(vects)
    rotangles = []
    for i in range(num - 1):
        pre_v = vects[i]
        next_v = vects[i + 1]
        # rotangle = Vect3d.angle(pre_v,next_v)
        rotangle = rot_angle(pre_v,next_v)
        rotangles.append(rotangle)
    return rotangles
def update_new_pose(pose_pts_arr,mocap_data):
    '''
    generate new pose
    :param pose_pts_arr:
    :param mocap_pts_arr:
    :return:
    '''
    leftHandLandmarks = mocap_data['landmark']
    # rightHandLandmarks = mocap_data['rightHandLandmarks']
    #
    # let
    # curTween = [
    # #// Lefthand landmarks
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// x
    # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// y
    # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// z
    # ],
    # #// Right handlandmarks
    # # [
    # #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// x
    # # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// y
    # # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, #// z
    # # ],
    # ]
    #
    # const
    # newTween = []
    # for landmark in leftHandLandmarks:
    #     newTween[leftHandLandmarks] = landmark.x
    #     newTween[leftHandLandmarks + 21] = landmark.y
    #     newTween[leftHandLandmarks + 42] = landmark.z
    # TweenMax.to(curTween[n], 1, {
    # overwrite: true,
    # ease: 'linear.easeNone',
    # immediate: true




    hand_mocap_indices = iClone_BoneData.hand_mocap_indices
    tpose_left_hand_indices = iClone_BoneData.tpose_left_hand_indices

    group_num = 5
    pose_pts_arr = np.array(pose_pts_arr)
    for i in range(group_num):
        pose_range = tpose_left_hand_indices[i]
        pose_pts = pose_pts_arr[pose_range[0]:pose_range[1]+1]
        pose_range_num = pose_range[1]-pose_range[0]+1

        mocap_pts_range = hand_mocap_indices[i]
        wrist = leftHandLandmarks[0]
        mocap_pts = []
        mocap_pts = leftHandLandmarks[mocap_pts_range[0]:mocap_pts_range[1]+1] # one finger mocap data
        mocap_pts.insert(0, wrist)
        vs = get_vecs(mocap_pts)
        poses = get_pose(vs)

        #left hand
        poses=np.array(poses)
        poses = -1*poses

        pose_start = tpose_left_hand_indices[i]
        if(pose_start[0]==40): #thumb
            pose_pts_arr[pose_start[0]] = pose_pts_arr[pose_start[0]]+np.array([0, 0, 0, 0, poses[0],0])
            pose_pts_arr[pose_start[0] + 1] = pose_pts_arr[pose_start[0] + 1]+np.array([0, 0, 0, 0, poses[1],0])
            pose_pts_arr[pose_start[0] + 2] = pose_pts_arr[pose_start[0] + 2]+np.array([0, 0, 0, 0, poses[2],0])
        else:
            pose_pts_arr[pose_start[0]] = pose_pts_arr[pose_start[0]]+np.array([0, 0, 0, 0, 0,poses[0]])
            pose_pts_arr[pose_start[0]+2] = pose_pts_arr[pose_start[0]+2]+np.array([0, 0, 0, 0, 0,poses[1]])
            pose_pts_arr[pose_start[0]+3] = pose_pts_arr[pose_start[0]+3]+np.array([0, 0, 0, 0, 0,poses[2]])

    return pose_pts_arr
def mocap_to_iclone(mocap_data):
    '''
    generate iclone format data from mocap json file
    :param tpose:
    :param json_file:
    :return:
    '''
    tpose = iClone_BoneData.tpose
    new_pose_pts_arr = update_new_pose(tpose, mocap_data)

    return new_pose_pts_arr


