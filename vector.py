from copy import copy
from cv2 import imshow
from matplotlib import image
from matplotlib.pyplot import flag
import numpy as np
import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

global wide
global long

capError = '错误：摄像头错误'

def to_int(point):
  point.x=point.x*wide
  point.y=point.y*long
  return point
def to_int2(x,y):
  return (int(x),int(y))

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print(capError+'Not Open.')
    exit()
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)as pose:
    flag_frist=False
    last_right={}
    while True:
        success, vido = cap.read()
        if not success:
            print(capError+'Cannot Read')
            print('再次尝试中')
            continue
        wide = vido.shape[1]
        long = vido.shape[0]
        vido.flags.writeable = False
        vido = cv.cvtColor(vido, cv.COLOR_BGR2RGB)
        result =pose.process(vido)
        landmarks=result.pose_landmarks.landmark
        left_shoulder=to_int(landmarks[12])
        right_shoulder=to_int(landmarks[11])
        right_hand=to_int(landmarks[19])
        left_hand=to_int(landmarks[20])
        if(not flag_frist):
          last_right=copy(right_hand)
          flag_frist=True
        vido.flags.writeable=True
        cv.line(vido,to_int2(left_shoulder.x,left_shoulder.y),to_int2(right_shoulder.x,right_shoulder.y),(255,0,0),2)
        cv.circle(vido,to_int2(right_hand.x,right_hand.y),3,(0,0,255),-1)
        cv.circle(vido,to_int2(left_hand.x,left_hand.y),3,(0,0,255),-1)
        vido=cv.cvtColor(vido, cv.COLOR_RGB2BGR)
        #if(flag_frist and abs(right_hand.x-last_right.x)>abs(left_shoulder.x-right_shoulder)):
        #  if(last_right.x):
        #    pass
        cv.imshow('vido', vido)
        if cv.waitKey(1) == ord('q'):
            break
cap.release()
