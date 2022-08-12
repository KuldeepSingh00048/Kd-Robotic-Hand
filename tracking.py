import cv2
import mediapipe as mp
import time
import serial
class handDetect():
    def __init__(self, mode= False,maxHands = 1, detectionCon=0.5,  trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = int(detectionCon)
        self.trackCon = int(trackCon)

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon,self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils


    def find_hand(self,frame, draw = True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if  draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame


    def find_position(self,frame, handNo = 0, draw = True):

        lmList = []
        if self.result.multi_hand_landmarks:
            myHand =  self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate ( myHand.landmark ):
                #print ( id, lm )
                h, w, c = frame.shape
                cx, cy = int ( lm.x * w ), int ( lm.y * h )
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle ( frame, (cx, cy), 7, (0, 255, 0), cv2.FILLED )
        return lmList

def main():
    pTime = 0
    cTime = 0
    webcam = cv2.VideoCapture(0)
    detector = handDetect()
    numOfValsRec = serial.Serial("COM4",9600)
    tippoint = [4, 8, 12, 16, 20]  #tippoint of 5 fingers( thumb=4, index=8, middle=12, ring=16, little=20)
    while True:
        ret, frame = webcam.read()
        frame = detector.find_hand (frame)
        lmList =  detector.find_position(frame, draw=False)
        if len(lmList) !=0:
            finger = []

            if lmList[tippoint[0]][1] > lmList[tippoint[0]-1][1]:
                finger.append ( 0 )
                #valRec.write('0')
            else:
                finger.append ( 1 )
                #valRec.write('1')

            for id in range(1,5):
                if lmList[tippoint[id]][2] < lmList[tippoint[id]-2][2]:
                    finger.append(0)
                    #valRec.write('0')
                else:
                    finger.append(1)
                    #valRec.write('1')
            print(finger)
            numOfValsRec.write(finger)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, 'FPS : '+ str(int(fps)), (3, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (192, 192, 192), 3)

        cv2.imshow('Hand tracking', frame)
        if cv2.waitKey(1) == 13:
            break

cv2.waitKey(0)
cv2.destroyAllWindows()

if __name__ =="__main__":
    main()


























