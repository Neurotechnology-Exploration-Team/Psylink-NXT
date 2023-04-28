import cv2
import mediapipe as mp
from datetime import datetime

def readMediaPipe(capture):
    pass
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    #Capture over rtsp
    #capture = "rtsp://10.118.34.26"

    #capture webcam
    #capture =

    # For webcam input:
    cap = cv2.VideoCapture(capture)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5, max_num_hands=1) as hands:
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        if results.multi_hand_world_landmarks:
          outList = []
          for hand_landmarks in results.multi_hand_world_landmarks:
            #print(str(type(hand_landmarks)) + "    " + str(hand_landmarks))
            f = open("mp_data.csv", 'w')
            f.write(str(datetime.now()))
            for landmark in hand_landmarks.landmark:
                 f.write(',')
                 f.write('{}|{}|{}'.format(landmark.x, landmark.y, landmark.z))
            f.write('\n')

