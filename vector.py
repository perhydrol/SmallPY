from copy import copy
from cv2 import imshow
from matplotlib import image
from matplotlib.pyplot import flag
import numpy as np
import cv2 as cv
import mediapipe as mp
from multiprocessing import Process, Pipe

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_hand = mp.solutions.hands

global wide
global long

capError = '错误：摄像头错误'


def to_int(point):
    point.x = point.x*wide
    point.y = point.y*long
    return point


def to_int2(x, y):
    return (int(x), int(y))


def Pose(p_vido: Pipe, p_res: Pipe):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)as pose:
        while (p_vido.poll(None)):
            vido = p_vido.recv()
            vido = cv.cvtColor(vido, cv.COLOR_BGR2RGB)
            result = pose.process(vido)
            if result.pose_landmarks:
              landmarks = result.pose_landmarks.landmark
              left_shoulder = landmarks[12]
              right_shoulder = landmarks[11]
              p_res.send([left_shoulder, right_shoulder])
            else:
              p_res.send([False])


def Hand(p_vido: Pipe, p_res: Pipe):
    with mp_hand.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while(p_vido.poll(None)):
            vido = p_vido.recv()
            vido = cv.cvtColor(vido, cv.COLOR_BGR2RGB)
            result = hands.process(vido)
            if result.multi_hand_landmarks:
              landmarks = result.multi_hand_landmarks[0].landmark
              res_hand = landmarks[0]
              p_res.send([res_hand])
            else:
              p_res.send([False])


if __name__ == '__main__':
    p1_send_par, p1_send_chil = Pipe()
    p1_rec_par, p1_rec_chil = Pipe()
    p2_send_par, p2_send_chil = Pipe()
    p2_rec_par, p2_rec_chil = Pipe()
    Pose_process = Process(target=Pose, args=(p1_send_chil, p1_rec_chil,))
    Hands_process = Process(target=Hand, args=(p2_send_chil, p2_rec_chil,))
    Pose_process.start()
    Hands_process.start()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print(capError+'Not Open.')
        exit()
    while True:
        success, vido = cap.read()
        if not success:
            print(capError+'Cannot Read')
            print('再次尝试中')
        vido.flags.writeable = False
        long = vido.shape[0]
        wide = vido.shape[1]
        p1_send_par.send(vido)
        p2_send_par.send(vido)
        shoulder = p1_rec_par.recv()
        hand = p2_rec_par.recv()[0]
        vido.flags.writeable=True
        if shoulder[0]!=False:
          to_int(shoulder[0]),to_int(shoulder[1])
          cv.line(vido,to_int2(shoulder[0].x,shoulder[1].y),to_int2(shoulder[1].x,shoulder[1].y),(225,0,0),3)
        if(not(hand==False)):
          to_int(hand)
          cv.circle(vido,to_int2(hand.x,hand.y),2,(225,0,0),-1)
        cv.imshow('test', cv.flip(vido, 1))
        if cv.waitKey(1) == ord('q'):
          Pose_process.terminate()
          Hands_process.terminate()
          break
    cap.release()
