from dataclasses import replace
import cv2
import mediapipe as mp
import numpy as np
import subprocess as sp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands

def lorR():
    cap = cv2.VideoCapture(0)
    flag_frist = True
    with mp_hand.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        loca = final = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print('Error')
                continue
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            wide = image.shape[1]
            long = image.shape[0]
            if result.multi_hand_landmarks:
                if(not flag_frist):
                    flag_frist = True
                for hand_landmarks in result.multi_hand_landmarks:
                    str_hand_xyz = str(hand_landmarks)
                    list_hand_xyz = str_hand_xyz.replace('{', '').replace('}', '').replace(
                        '\n', '').replace(' ', '').split('landmark')
                    list_hand_xyz = list_hand_xyz[1]
                    # print(list_hand_xyz,file=open('out.txt','a'))
                    temp = list_hand_xyz.replace('x:', 'k').replace(
                        'y:', 'k').replace('z:', 'k').split('k')[1]
                    temp = float(temp)*wide
                    if(temp <= 200 or temp >= 500):
                        if(loca == 0):
                            loca = temp
                        else:
                            final = temp
                    # print(temp)

            else:
                if(flag_frist):
                    if(abs(loca-final)) > 300:
                        cap.release()
                        return loca-final
                    else:
                        flag_frist = False
                        loca = final = 0
                        continue


while(True):
    x = lorR()
    if(x < -300):
        print('left')
        sp.run(['last.exe'])
    elif(x > 300):
        print('right')
        sp.run(['next.exe'])
    else:
        print('cannot')
