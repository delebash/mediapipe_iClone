'''
generate new pose from left hand mocap data
'''
import json
import numpy as np
tpose = [
          0, 105, 0, 0, 0, 0,       #hips                   [0]
          -11, 105, 0, 0, 0, 0,
          -11, 56, 0, 0, 0, 0,
          -11, 8, 0, 0, 0, 0,
          11, 105, 0, 0, 0, 0,
          11, 56, 0, 0, 0, 0,
          11, 8, 0, 0, 0, 0.0,
          0, 118, 0, 0, 0, 0,       #spine                  [7]
          0, 129, 0, 0, 0, 0,
          0, 141, 0, 0, 0, 0,
          0, 152, 0, 0, 0, 0,
          0, 164, 0, 0, 0, 0,
          0, 173, 0, 0, 0, 0,
          -3, 160, 0, 0, 0, 0,      #right_shoulder         [13]
          -17, 160, 0, 0, 0, 0,
          -46, 160, 0, 0, 0, 0,
          -74, 160, 0, 0, 0, 0,     #right_hand             [16]

          -77, 161, 3, 0, 30, 0,    #right_hand_thumb_1     [17]
          -81, 161, 3, 0, 0, 0,
          -83, 161, 3, 0, 0, 0,
          -78, 161, 2, 0, 0, 0,     #right_in_hand_index    [20]
          -83, 161, 3, 0, 0, 0,
          -87, 161, 3, 0, 0, 0,
          -89, 161, 3, 0, 0, 0,
          -78, 161, 0, 0, 0, 0,     #right_in_hand_middle   [24]
          -83, 161, 1, 0, 0, 0,
          -88, 161, 1, 0, 0, 0,
          -90, 161, 1, 0, 0, 0,
          -78, 161, -0, 0, 0, 0,    #right_in_hand_ring     [28]
          -83, 161, -0, 0, 0, 0,
          -86, 161, -0, 0, 0, 0,
          -89, 161, -0, 0, 0, 0,
          -77, 161, -1, 0, 0, 0,    #right_in_hand_pinky    [32]
          -82, 161, -2, 0, 0, 0,
          -85, 161, -2, 0, 0, 0,
          -87, 161, -2, 0, 0, 0,

          3, 160, 0, 0, 0, 0,       #left_shoulder          [36]
          17, 160, 0, 0, 0, 0,
          46, 160, 0, 0, 0, 0,
          74, 160, 0, 0, 0, 0,      #left_hand              [39]

          # 77, 161, 3, 0, -30, 0,    # left_hand_thumb_1      [40]
          77, 161, 3, 0, -30, 0,    # left_hand_thumb_1      [40]
          81, 161, 3, 0, 0, 0,
          83, 161, 3, 0, 0, 0,
          78, 161, 2, 0, 0, 0,      # left index                   [43]
          83, 161, 3, 0, 0, 0,
          87, 161, 3, 0, 0, 0,
          89, 161, 3, 0, 0, 0,
          78, 161, 0, 0, 0, 0,      #left middle                  [47]
          83, 161, 1, 0, 0, 0,
          88, 161, 1, 0, 0, 0,
          90, 161, 1, 0, 0, 0,
          78, 161, 0, 0, 0, 0,      # left ring                   [51]
          83, 161, 0, 0, 0, 0,
          86, 161, 0, 0, 0, 0,
          89, 161, 0, 0, 0, 0,
          77, 161, -1, 0, 0, 0,     # left pinky                  [55]
          82, 161, -2, 0, 0, 0,
          85, 161, -2, 0, 0, 0,
          87, 161, -2, 0, 0, 0]

def gen_row_6(tpose):
    '''
    generate mocap rows data
    :param tpose:
    :return:
    '''
    num = len(tpose)
    pts_num = num/6
    pose_arr = []
    for i in range(1,num,6):
        pt = []
        for j in range(i-1,i+5):
            pt.append(tpose[j])
        pose_arr.append(pt)
    return pose_arr

def gen_mocap_pt_arr(json_data):
    '''
    #generate mocap pts arr
    :param json_file:
    :return:
    '''
    # read file
    mocap_pts_arr = []

    for finger in json_data:
        finger_joints = finger['points']
        for pt in finger_joints:
            mocap_pts_arr.append(pt)
    return mocap_pts_arr


def get_vecs(mocap_data):
    '''
    generate vetors
    :param mocap_data:
    :return:
    '''
    num = len(mocap_data)
    vects = []
    for i in range(num - 1):
        pre_pt = np.array(mocap_data[i])
        next_pt = np.array(mocap_data[i + 1])
        vec = np.array(next_pt) - np.array(pre_pt)
        vec = vec/np.linalg.norm(vec)
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
        rotangle = rot_angle(pre_v,next_v)
        rotangles.append(rotangle)
    return rotangles
def update_new_pose(pose_pts_arr,mocap_pts_arr):
    '''
    generate new pose
    :param pose_pts_arr:
    :param mocap_pts_arr:
    :return:
    '''
    #pose_pts_ind = [[17,19],[20,23],[24,27],[28,31],[32,35]] #right hand
    pose_pts_ind = [[40,42], [43,46], [47,50], [51,54], [55,58]] #left hand
    mocap_pts_ind = [[0,4],[5,9],[10,14],[15,19],[20,24]]
    group_num = 5
    pose_pts_arr = np.array(pose_pts_arr)
    for i in range(group_num):
        pose_range = pose_pts_ind[i]
        pose_pts = pose_pts_arr[pose_range[0]:pose_range[1]+1]
        pose_range_num = pose_range[1]-pose_range[0]+1

        mocap_pts_range = mocap_pts_ind[i]
        mocap_pts = mocap_pts_arr[mocap_pts_range[0]:mocap_pts_range[1]+1] # one finger mocap data

        vs = get_vecs(mocap_pts)
        poses = get_pose(vs)

        #left hand
        poses=np.array(poses)
        poses = -1*poses

        pose_start = pose_pts_ind[i]
        if(pose_start[0]==40): #thumb
            pose_pts_arr[pose_start[0]] = pose_pts_arr[pose_start[0]]+np.array([0, 0, 0, 0, poses[0],0])
            pose_pts_arr[pose_start[0] + 1] = pose_pts_arr[pose_start[0] + 1]+np.array([0, 0, 0, 0, poses[1],0])
            pose_pts_arr[pose_start[0] + 2] = pose_pts_arr[pose_start[0] + 2]+np.array([0, 0, 0, 0, poses[2],0])
        else:
            pose_pts_arr[pose_start[0]] = pose_pts_arr[pose_start[0]]+np.array([0, 0, 0, 0, 0,poses[0]])
            pose_pts_arr[pose_start[0]+2] = pose_pts_arr[pose_start[0]+2]+np.array([0, 0, 0, 0, 0,poses[1]])
            pose_pts_arr[pose_start[0]+3] = pose_pts_arr[pose_start[0]+3]+np.array([0, 0, 0, 0, 0,poses[2]])

    return pose_pts_arr
def json2iclon(json_data):
    '''
    generate iclone format data from mocap json file
    :param tpose:
    :param json_file:
    :return:
    '''

    pose_pts_arr = gen_row_6(tpose)
    mocap_pts_arr = gen_mocap_pt_arr(json_data)

    # print("pose data:")
    # for pose_pt in pose_pts_arr:
    #     print(pose_pt)
    # print("mocap data:")
    # for mocap_pt in mocap_pts_arr:
    #     print(mocap_pt)

    new_pose_pts_arr = update_new_pose(pose_pts_arr,mocap_pts_arr)

    # arr_num = len(new_pose_pts_arr)
    # for k in range(arr_num):
    #     pts = new_pose_pts_arr[k]
    #     for n in range(6):
    #         print(pts[n],",",end="")
    #     print("\n")

    return new_pose_pts_arr


