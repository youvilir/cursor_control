import cv2
import numpy as np
import back.HandTrackingModule as htm
import time
import autopy
import pyautogui
import device
from enum import IntEnum

class Gest(IntEnum):
    """enumeration for gest

    Args:
        IntEnum (int): 
        Index_Thumb_Up - Index and Thumb fingers are up - LEFT CLICK or DOUBLE CLICK
        Index_Up - Only Index finger is up - MOVING CURSOR
        Index_Middle_Up - Index and Middle fingers are up - RIGHT CLICK
        Index_Little_Up - Index and little fingers are up - DRAG AND DROP
    """
    Index_Thumb_Up = 0
    Index_Up = 1
    Index_Middle_Up = 2
    Index_Little_Up = 4

#############################

class Controller:
    tx_old = 0
    ty_old = 0
    trial = True
    flag = False
    grabflag = False
    pinchmajorflag = False
    pinchminorflag = False
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 1
    
    def getpinchylv(hand_result):
        dist = round((Controller.pinchstartycoord - hand_result.landmark[4].y),1)
        return dist

    def getpinchxlv(hand_result):
        dist = round((hand_result.landmark[4].x - Controller.pinchstartxcoord),1)
        return dist
    
    
    def scrollVertical():
        print("In scroll")
        #mouse.scroll(0, 100 if Controller.pinchlv>0.0 else -100)
        print(Controller.pinchlv)
        pyautogui.scroll(50 if Controller.pinchlv>0.0 else -50)
        
    
    def scrollHorizontal():
        print("in hscroll")
        #mouse.scroll(-100 if Controller.pinchlv>0.0 else 100, 0)
        #pyautogui.hscroll(50 if Controller.pinchlv>0.0 else -50)

        pyautogui.keyDown('shift')
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(-120 if Controller.pinchlv>0.0 else 120)
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')

    def pinch_control_init(hand_result):
        Controller.pinchstartxcoord = hand_result.landmark[4].x
        Controller.pinchstartycoord = hand_result.landmark[4].y
        Controller.pinchlv = 0
        Controller.prevpinchlv = 0
        Controller.framecount = 0

    # Hold final position for 5 frames to change status
    def pinch_control(hand_result, controlHorizontal, controlVertical):
        #print("pinch_control")
        if Controller.framecount == 5:
            
            Controller.framecount = 0
            Controller.pinchlv = Controller.prevpinchlv

            if Controller.pinchdirectionflag == True:
                print("controlHorizontal")
                controlHorizontal() #x

            elif Controller.pinchdirectionflag == False:
                print("controlVertical")
                controlVertical() #y

        lvx =  Controller.getpinchxlv(hand_result)
        lvy =  Controller.getpinchylv(hand_result)
        print(Controller.prevpinchlv - lvy)
            
        if abs(lvy) > abs(lvx):
            Controller.pinchdirectionflag = False
            if abs(Controller.prevpinchlv - lvy) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvy
                Controller.framecount = 0

        elif abs(lvx) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = True
            if abs(Controller.prevpinchlv - lvx) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvx
                Controller.framecount = 0

############################

class VirtualMouse():

    devices = device.getDeviceList()
    
    pyautogui.FAILSAFE = False
    ##############################

    wCam, hCam = 640, 480
    smoothening = 10
    frameRValue = 1
    frameR = 100 * frameRValue # Frame Redaction
    ##############################

    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    #############################

    lastValueForThumbFinger = 0
    lastValueForIndexFinger = 0
    lastValueForMiddleFinger = 0
    lastValueForLittleFinger = 0

    #############################
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(3, wCam) #width
    cap.set(4, hCam) #height
    cap.set(cv2.CAP_PROP_FPS, 60)
    detector = htm.handDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()

    ##############################

    LeftClick = False
    RightClick = False
    DBLefrClick = False
    DragAndDrop = False
    Scrolling = False

    #############################

    fps = 30

    #############################

    drawing_landmarks = False
    
    def SetCamera(i):
        try:
            if VirtualMouse.cap:
                VirtualMouse.cap.release()

            VirtualMouse.cap.open(i)
        except:
            pass


    def GestureRecognition(fingers):
        """Gesture recognition

        Args:
            fingers (int[]): fingers array (example - [0,1,0,0,0])

        Returns:
            number of gest or None if gest is not defined
        """
        if fingers[1]:

            if sum(fingers) == 1:
                
                return Gest(1)

            elif sum(fingers) == 2:

                if fingers[0]:

                    return Gest(0)

                elif fingers[2]:

                    return Gest(2)

                elif fingers[4]:

                    return Gest(4)
        else:
            return None
        
    def MouseAction(gest, lmsList, img):
        """perform a mouse action on a gesture

        Args:
            gest (Gest): number of gest
            lmsList (_type_): coordinates of landmarks
            img (img): image from camera
        """

        if gest == Gest.Index_Up:

            x1, y1 = lmsList[8][1:]

            x3 = np.interp(x1, (VirtualMouse.frameR, VirtualMouse.wCam - VirtualMouse.frameR) , (0, VirtualMouse.wScr))
            y3 = np.interp(y1, (VirtualMouse.frameR, VirtualMouse.hCam - VirtualMouse.frameR) , (0, VirtualMouse.hScr))

            # 6. Smoothen Value

            VirtualMouse.clocX = VirtualMouse.plocX + (x3 - VirtualMouse.plocX) / VirtualMouse.smoothening
            VirtualMouse.clocY = VirtualMouse.plocY + (y3 - VirtualMouse.plocY) / VirtualMouse.smoothening

            # 7. Move Mouse
            
            autopy.mouse.move(VirtualMouse.wScr - VirtualMouse.clocX, VirtualMouse.clocY)
            #cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
            VirtualMouse.plocX, VirtualMouse.plocY = VirtualMouse.clocX, VirtualMouse.clocY

            if VirtualMouse.lastValueForThumbFinger :
                        
                if VirtualMouse.DBLefrClick :
                
                    autopy.mouse.click()
                    autopy.mouse.click()
                    
                    VirtualMouse.DBLefrClick = False
                    VirtualMouse.LeftClick = False

                elif VirtualMouse.LeftClick :
                
                    autopy.mouse.click()
                    VirtualMouse.LeftClick = False

                VirtualMouse.lastValueForThumbFinger = 0

            elif VirtualMouse.lastValueForMiddleFinger :
                        
                autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)

                VirtualMouse.lastValueForMiddleFinger = 0

            if VirtualMouse.lastValueForLittleFinger :
                    
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)

                VirtualMouse.lastValueForLittleFinger = 0

        elif gest == Gest.Index_Thumb_Up:

            # 9. Find distance between fingers

            length, img, lineInfo = VirtualMouse.detector.findDistance(6, 4, img)
            print(length)

            #if the Thumb touches the index finger: double left click

            if length < 30:
                VirtualMouse.DBLefrClick = True

            #if the Thumb finger is up: left click

            else:
                VirtualMouse.LeftClick = True

            VirtualMouse.lastValueForThumbFinger = 1

        elif gest == Gest.Index_Middle_Up:

            VirtualMouse.RightClick = True
            VirtualMouse.lastValueForMiddleFinger = 1

        elif gest == Gest.Index_Little_Up:

            VirtualMouse.DragAndDrop = True
            VirtualMouse.lastValueForLittleFinger = 1

    def Show_image():
        # 1. Find hand Landmarks
        assert(VirtualMouse.cap)

        success, img = VirtualMouse.cap.read()
        if not success:
            print("not success")
            return success, img

        img = VirtualMouse.detector.findHands(img,draw=VirtualMouse.drawing_landmarks)
        lmsList, bbox = VirtualMouse.detector.findPosition(img,draw=False)

        # 3. Check which fingers are up
        fingers = VirtualMouse.detector.fingersUp()
        cv2.rectangle(img, (VirtualMouse.frameR, VirtualMouse.frameR), 
                        (VirtualMouse.wCam - VirtualMouse.frameR , VirtualMouse.hCam - VirtualMouse.frameR), 
                        (255,0,255), 2)
        # 4. Only Index finger : Moving Mode
        if len(fingers):
        
            try:
                gest = VirtualMouse.GestureRecognition(fingers)
                VirtualMouse.MouseAction(gest,lmsList,img)
            except:
                pass
        # 11. Frame Rate
        VirtualMouse.cTime = time.time()
        VirtualMouse.fps = 1/(VirtualMouse.cTime - VirtualMouse.pTime)
        VirtualMouse.pTime = VirtualMouse.cTime
        cv2.putText(img, str(int(VirtualMouse.fps)), (18,78), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        # 12. Display
        return success,img


    def Start():
        print("Virtual mouse activeted")

        while VirtualMouse.cap.isOpened():

            # 1. Find hand Landmarks
            success, img = VirtualMouse.cap.read()
            
            if not success:
                break

            img = VirtualMouse.detector.findHands(img,draw=True)
            lmsList, bbox = VirtualMouse.detector.findPosition(img,draw=False)

            # 3. Check which fingers are up
            fingers = VirtualMouse.detector.fingersUp()

            cv2.rectangle(img, (VirtualMouse.frameR, VirtualMouse.frameR), 
                            (VirtualMouse.wCam - VirtualMouse.frameR , VirtualMouse.hCam - VirtualMouse.frameR), 
                            (255,0,255), 2)

            # 4. Only Index finger : Moving Mode
            if len(fingers):
            

                try:
                    gest = VirtualMouse.GestureRecognition(fingers)
                    VirtualMouse.MouseAction(gest,lmsList,img)

                except:
                    pass


            # 11. Frame Rate
            VirtualMouse.cTime = time.time()
            fps = 1/(VirtualMouse.cTime - VirtualMouse.pTime)

            VirtualMouse.pTime = VirtualMouse.cTime

            cv2.putText(img, str(int(fps)), (18,78), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

            # 12. Display
            cv2.imshow("Image", img)
            
            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                cv2.destroyAllWindows()
                break
               
