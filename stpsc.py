import random

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import keyword

init_timer = 0
cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

detector  = HandDetector(maxHands=1)

timer = 0
stateResult = False
gameStart = False

total_scores = [0, 0]


while (True):
    imgBG = cv2.imread("./background.png")
    success , img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.500,0.500)
    imgScaled =imgScaled[:,80:460]



    #Find Hands
    hands , img = detector.findHands(imgScaled)




    if (gameStart):

        #  Starting counts
        if stateResult == False:
            timer = time.time() - init_timer
            cv2.putText(imgBG,str(int(timer)),(518,418),cv2.FONT_HERSHEY_PLAIN,6, (0,255,40),4 )

        if timer>3 :
            stateResult=True
            timer= 0
            playerMove=0
            if hands:
                player_input = 0
                hand= hands[0]

                fingers =detector.fingersUp(hand)
                if fingers == [0, 0, 0, 0, 0]:
                    playerMove = 1   # stone
                if fingers == [1, 1, 1, 1, 1]:
                    playerMove = 2     # paper
                if fingers == [0, 1, 1, 0, 0]:
                    playerMove = 3      # scissor


    #             Computer side game
                randomNumber = random.randint(1,3)
                get_img = cv2.imread(f'computer_chance/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                # imgBG = cvzone.overlayPNG(imgBG, get_img,[0,0])
                # imgBG[110:, 240:] = get_img

                print(randomNumber)

                # player Winer
                if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                    total_scores[1] += 1

                # computer Winer
                if (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                    total_scores[0] += 1

    imgBG[234:504,644:1024]= imgScaled # Calculate 540 - 80*2 = diff ... similarly   or hiit and try

    # if stateResult:
    #     # imgBG = cvzone.overlayPNG(imgBG, get_img, (0,0))


    cv2.putText(imgBG, str(total_scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0,255), 6)
    cv2.putText(imgBG, str(total_scores[1]), (890, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 6)


    cv2.imshow("image",imgBG)
    # cv2.imshow("scaled",imgScaled)
    key = cv2.waitKey(1)

    # STARTING GAME
    if key ==ord(' '):
        gameStart= True
        init_timer = time.time()
        stateResult=False