import cv2
import mediapipe as mp
from datetime import datetime

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#Capture over rtsp
capture = "rtsp://10.118.34.26"

#capture webcam
#capture =


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

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_world_landmarks:
      outList = [[] for i in range(21)]
      for hand_landmarks in results.multi_hand_world_landmarks:
        #print(str(type(hand_landmarks)) + "    " + str(hand_landmarks))
        f = open("mp_data.csv", 'w')
        f.write(str(datetime.now()))
        for landmark in hand_landmarks.landmark:
             f.write(',')
             f.write('{}|{}|{}'.format(landmark.x, landmark.y, landmark.z))
        f.write('\n')
            
            #print(str(type(landmark.x)) + "     " + str(landmark.x))
       # print(outList)
        
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()



