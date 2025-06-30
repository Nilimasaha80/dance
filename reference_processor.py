# src/reference_processor.py
import cv2, mediapipe as mp, json

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def process_teacher(video_path, out_json):
    cap = cv2.VideoCapture(video_path)
    data = []
    with mp_holistic.Holistic() as holistic:
        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret: break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = holistic.process(img)
            if res.pose_landmarks and res.face_landmarks and res.left_hand_landmarks and res.right_hand_landmarks:
                data.append({
                    'frame': idx,
                    'pose': [(lm.x, lm.y, lm.z) for lm in res.pose_landmarks.landmark],
                    'face': [(lm.x, lm.y, lm.z) for lm in res.face_landmarks.landmark],
                    'lh': [(lm.x, lm.y, lm.z) for lm in res.left_hand_landmarks.landmark],
                    'rh': [(lm.x, lm.y, lm.z) for lm in res.right_hand_landmarks.landmark],
                })
            idx += 1
    with open(out_json, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    process_teacher('teacher.mp4', '../models/adavu1_ref.json')
