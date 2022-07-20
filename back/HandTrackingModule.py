import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
           
    def __init__(self, mode=False, maxHands=2, complexity = 1,
                detectionCon=0.8, trackCon=0.5):
        """ctor

        Args:
            mode (bool, optional): Whether to treat the input images as a batch of static and possibly unrelated images, or a video stream. Defaults to False.
            maxHands (int, optional): Maximum number of hands to detect. Defaults to 2.
            complexity (int, optional): Complexity of the hand landmark model: 0 or 1. Defaults to 1.
            detectionCon (float, optional): Minimum confidence value ([0.0, 1.0]) for hand detection to be considered successful. Defaults to 0.8.
            trackCon (float, optional): Minimum confidence value ([0.0, 1.0]) for the hand landmarks to be considered tracked successfully. Defaults to 0.5.
        """

        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        # массив из ориентиров пальцев руки
        self.tipIds = [4, 8, 12, 16, 20] 
        self.prev_hand = None
        

    def findHands(self, img, draw=True): 
        """find hands in the image

        Args:
            img (image): image on which you need to find hands
            draw (bool, optional): drawing hand landmarks. Defaults to True.

        Returns:
            image
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    #нахождение позиции ориентиров пальцев руки
    def findPosition(self, img, handNo=0, draw=True):
        """fing position of hand_landmark

        Args:
            img (image): image on which you need to find landmarks
            handNo (int, optional): number of hand. Defaults to 0.
            draw (bool, optional): drawing landmarks. Defaults to True.

        Returns:
            _type_: _description_
        """
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        self.Hand = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            self.Hand = myHand
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                #print(id, lm)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox


    def fingersUp(self):
        """finding raised fingers

        Returns:
            massive[]: array of 5 elements(fingers), 0 - finger is down, 1 - finger is up
        """

        fingers = []
        # Thumb
        if(len(self.lmList))!=0:

            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 2][1]:

                fingers.append(1)
            else:
                fingers.append(0)

        # Fingers

            for id in range(1, 5):

                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers

    #нахождение дистанции между двумя пальцами
    def findDistance(self, p1, p2, img, draw=True,r=10, t=3):
        """find distance between two landmarks

        Args:
            p1 (int): first landmark
            p2 (int): second landmark
            img (image): image on which you need to find distance between two landmarks
            draw (bool, optional): drawing landmarks. Defaults to True.
            r (int, optional): radius of circle that drawing. Defaults to 15.
            t (int, optional): line thickness between two landmarks. Defaults to 3.

        Returns:
            length: int - distance between two landmarks
            img: image
            massive: int[]
        """

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        
        print(detector.fingersUp())

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()