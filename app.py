# src/app.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2, mediapipe as mp, numpy as np, pyttsx3
from angles import angle
import json

RTC_CONFIGURATION = RTCConfiguration({"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]})

class AgentProcessor(VideoProcessorBase):
    def __init__(self):
        self.holistic = mp.solutions.holistic.Holistic()
        self.ref = json.load(open("models/adavu1_ref.json"))
        self.idx = 0
        self.tts = pyttsx3.init()
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        res = self.holistic.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if res.pose_landmarks:
            # compute one example angle, compare to ref, overlay & speak
            lm = res.pose_landmarks.landmark
            a,b,c = lm[mp.solutions.holistic.PoseLandmark.RIGHT_SHOULDER.value], \
                   lm[mp.solutions.holistic.PoseLandmark.RIGHT_ELBOW.value], \
                   lm[mp.solutions.holistic.PoseLandmark.RIGHT_WRIST.value]
            user_ang = angle((a.x,a.y),(b.x,b.y),(c.x,c.y))
            ref_ang = ...
            cv2.putText(img, f"{int(user_ang)}°", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,255,0) if abs(user_ang - ref_ang)<15 else (0,0,255), 2)
            if abs(user_ang - ref_ang)>15:
                self.tts.say("Raise your elbow")
                self.tts.runAndWait()
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Bharatanatyam AI Agent")
    webrtc_streamer(key="agent", mode="sendrecv",
                    video_processor_factory=AgentProcessor,
                    rtc_configuration=RTC_CONFIGURATION)
