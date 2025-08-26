#Run this with pycharm or other IDE using python 3.12
# This sends data to serial port of thonny receive script (saved as main.py) 
import time
#time.sleep(1)
import cv2
import mediapipe as mp
import serial

pico = serial.Serial('COM3', 115200)  # Adjust as needed
#time.sleep(1)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger landmarks
            tips = [
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            ]

            mcps = [
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP],
                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            ]
            finger_states = ''
            for i in range(5):
                try:
                    if i == 0:
                        state = tips[i].x > mcps[i].x
                    else:
                        state = tips[i].y < mcps[i].y
                    finger_states += '1' if state else '0'
                except:
                    finger_states += '0'
            print(f"Finger States: {finger_states}")  # <- print AFTER loop finishes
            time.sleep(0.2)
            pico.write((finger_states + '\n').encode())

    flipped_frame = cv2.flip(frame, 1)
    cv2.imshow('Hand Tracking', flipped_frame)
    #cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
