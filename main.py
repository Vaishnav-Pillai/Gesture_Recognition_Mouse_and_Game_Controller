import cv2
import mediapipe as mp
import pyautogui
import subprocess
import sys

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y=0
index_x=0
thumb_x=0
thumb_y=0
fist_detected = False

while(True):
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            # print(landmarks[0])
            for id,landmark in enumerate(landmarks):
                x=int(landmark.x * frame_width)
                y=int(landmark.y * frame_height)
                # print(landmark.x,landmark.y)

                if id==0:
                    wrist_x = screen_width/frame_width * x
                    wrist_y = screen_height/frame_height * y
                    # print(thumb_x - wrist_x,index_y - wrist_y)
                    if((wrist_x - thumb_x)<200 and (wrist_y - index_y)<200):
                        print("Fist detected!")
                        subprocess.Popen([sys.executable, "gameControl.py"])
                        cap.release()
                        cv2.destroyAllWindows()
                        sys.exit()

                if id==8:
                    cv2.circle(frame,(x,y),15,(0,255,255))
                    index_x = screen_width/frame_width * x
                    index_y = screen_height/frame_height * y
                    pyautogui.moveTo(index_x,index_y)

                if id==4:
                    cv2.circle(frame,(x,y),15,(0,255,255))
                    thumb_x = screen_width/frame_width * x
                    thumb_y = screen_height/frame_height * y
                    # print(abs(index_y - thumb_y))
                    # print(abs((((index_x - thumb_x) ** 2) + ((index_y - thumb_y) ** 2)) ** 0.5))
                    if abs(index_y - thumb_y) < 100:
                        # print('Hold')
                        pyautogui.mouseDown()

                    if abs(index_y - thumb_y) > 100:
                        # print('Release')
                        pyautogui.mouseUp()

                if id==12:
                    cv2.circle(frame,(x,y),15,(0,255,255))
                    middle_x = screen_width/frame_width * x
                    middle_y = screen_height/frame_height * y
                    if abs(index_x - middle_x) < 100:
                        # print('Clicked')
                        pyautogui.click()
                        pyautogui.sleep(1)
                
                if id==16:
                    cv2.circle(frame,(x,y),15,(0,255,255))
                    ring_x = screen_width/frame_width * x
                    ring_y = screen_height/frame_height * y
                    # print(abs(thumb_y - ring_y))

                    if abs(thumb_x - ring_x) < 30:
                        # print('Double Click')
                        pyautogui.click(clicks=2)
                        pyautogui.sleep(1)

                if id==20:
                    cv2.circle(frame,(x,y),15,(0,255,255))
                    pinky_x = screen_width/frame_width * x
                    pinky_y = screen_height/frame_height * y
                    # print(abs(thumb_x - pinky_x))

                    if abs(thumb_x - pinky_x) < 50:
                        # print('Right Click')
                        pyautogui.click(button='right')
                        pyautogui.sleep(1)
    
    cv2.imshow('Personal Mouse', frame)
    cv2.waitKey(1)