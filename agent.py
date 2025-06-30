# src/agent.py
import cv2, mediapipe as mp, json
import numpy as np
from angles import angle
import pyttsx3

engine = pyttsx3.init()
mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

# Load reference
with open('../models/adavu1_ref.json') as f:
    ref = json.load(f)

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic() as holistic:
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = holistic.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            # Example: right elbow angle
            a = lm[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]
            b = lm[mp_holistic.PoseLandmark.RIGHT_ELBOW.value]
            c = lm[mp_holistic.PoseLandmark.RIGHT_WRIST.value]
            user_ang = angle((a.x, a.y), (b.x, b.y), (c.x, c.y))

            ref_frame = ref[idx % len(ref)]
            ra = ref_frame['pose'][mp_holistic.PoseLandmark.RIGHT_ELBOW.value]
            rb = ref_frame['pose'][mp_holistic.PoseLandmark.RIGHT_WRIST.value]
            rc = ref_frame['pose'][mp_holistic.PoseLandmark.RIGHT_SHOULDER.value]
            ref_ang = angle(rc, ra, rb)

            cv2.putText(img, f"{int(user_ang)}°", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if abs(user_ang-ref_ang)<15 else (0,0,255), 2)
            if abs(user_ang-ref_ang)>15:
                engine.say("Raise your elbow")
                engine.runAndWait()

        mp_draw.draw_landmarks(img, res.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        mp_draw.draw_landmarks(img, res.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_draw.draw_landmarks(img, res.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(img, res.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        cv2.imshow("Agent", img)
        idx += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
