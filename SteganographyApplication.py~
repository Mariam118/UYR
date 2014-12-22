#!/usr/bin/python
##############################################################################################################

import os
import sys
import cv2
import shutil
import cv2.cv as cv
from LSBSteg import LSBSteg
##############################################################################################################

positionList = []
###########################################################################################---Function to search for char in frame
def foundChar(msgC, Fnum): 

    k=0
    imgName = "tmp/frame%d.jpg" % Fnum
    #data="None"
    try:
        imageFile = imgName
        data = open(imageFile, "rb").read()
    except IOError:
        print "Image file %s not found" % imageFile
        raise SystemExit

    Num = ord ( msgC ) 
    hexNum = hex(Num)[2:]
    for ch in data:
        # make a hex byte
        byt = "%02X" % ord(ch)
	#if hexNum == byt:
        if ord(ch) == Num:
            loc = k
            positionList.append(  (Fnum + k, ",")  )  # should remove byte
            return True
        k = k+1
    return False
###########################################################################################---Function to search for char in frame
#
#
########################################################################################################---Message Hiding Function 
def hideMSG():
#--------------------------------------------------------
#Read the MSG

    secMSG= raw_input('Please enter the message:')           #print (secMSG)
    msgLen = len(secMSG)                                     #print (msgLen)

    if msgLen/24/60 == 0:
        print ("{} :{} minutes".format("Please select video file, minimum time is",1) )
    else:
        print ("{} :{} minutes".format("Please select video file, minimum time is",msgLen/24/60*2) )



#--------------------------------------------------------
#Read Video and
#check if video frame number is enough

    enoughSize = True

    while  enoughSize:

        absPath= raw_input('Please enter the video path:')        #print (absPath)
        vidcap = cv2.VideoCapture(absPath)                        #print ("success")
    
        frameNumbers = vidcap.get ( cv.CV_CAP_PROP_FRAME_COUNT )  #print ( frameNumbers )
        fps =  vidcap.get (cv.CV_CAP_PROP_FPS)                    #print ( fps )
        videoLength = frameNumbers / fps    # seconds             #print ( videoLength )

        count = 0;

        if videoLength < msgLen/24*2:                                                                 
            print (" no enough space to embed the message, try another video (more time)")
	    n= raw_input('press n to try another video or any other key to exit:')
	    if n != "n":
	        sys.exit()
        else: 
            enoughSize = False
    	    success,image = vidcap.read()
            os.mkdir('tmp') 
	    while success:
                success,image = vidcap.read()
                cv2.imwrite("tmp/frame%d.jpg" % count, image)     # save frame as JPEG file
                count += 1
                #print ( count )


#--------------------------------------------------------------------------------------------
#split msg char, search and create positions for chars

    msgList = list ( secMSG )
    c = 0

    found = False
    for msgChar in msgList:
        while found <> True:
            found=foundChar( msgChar , c )
            c=(c+1)%count
        found = False


#---------------------------------------------------------------------
# Write posetions list to a text file

    tmpFile = open("tmp/tmpFile.txt", "w")
    tmpFile.write('\n'.join('%s %s' % x for x in positionList))
    tmpFile.close()

#---------------------------------------------------------------------
# read from file and save in string

    dataEm =""
    for line in open("tmp/tmpFile.txt"):
        words = line.strip().split(',')
        dataEm = dataEm + " " + words[0]
        dataEm = dataEm + "\n"

 
    imgAbsPath= raw_input('Please enter the image path:')               

    pathList = imgAbsPath.split("/")
    imgNameJPG = pathList[-1]

    imgName = imgNameJPG.split(".")

    carrier = cv.LoadImage(imgAbsPath)
    steg = LSBSteg(carrier)
    steg.hideText( dataEm )  
    imgNamePNG = imgName[0]+".png"
    print (imgNamePNG + " is the chracter map")
    steg.saveImage(imgNamePNG)

    print ("Hidden successfully")
    shutil.rmtree('tmp')
    sys.exit()

#---------------------------------------------------------------------


#######################################################################################################---Message Hiding Function 
#
#
######################################################################################################---Message Extracting Function
def extractMSG():
#--------------------------------------------------------------------- 
# Extract from picture

    imgAbsPath= raw_input('Please enter the image path:')             

    im = cv.LoadImage(imgAbsPath)
    steg = LSBSteg(im)
    #print "Text value:",steg.unhideText()
    s=steg.unhideText()
    os.mkdir('tmp')
    tmpFile = open("tmp/PositionsList.txt", "w")
    tmpFile.write(s)
    tmpFile.close()
#---------------------------------------------------------------------  
#Read Video file frames

    absPath= raw_input('Please enter the video path:')        #print (absPath)
    vidcap = cv2.VideoCapture(absPath)                        #print ("success")

    count=0
    success,image = vidcap.read()
    while success:
        success,image = vidcap.read()
        cv2.imwrite("tmp/frame%d.jpg" % count, image)     # save frame as JPEG file
        count += 1

#--------------------------------------------------------------------- 
# extract message from frames
   
    fNum = 0
    secMSG=""
    for line in open("tmp/PositionsList.txt"):
        word = int(line.strip())
        cPos = word - fNum
        imgName = "tmp/frame%d.jpg" % fNum
        try:
            imageFile = imgName
            data = open(imageFile, "rb").read()
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit

        msgOrd = data[ cPos ]
        secMSG = secMSG + msgOrd
        fNum = fNum + 1

        
    shutil.rmtree('tmp')
    print ("secret message is: "+secMSG)
#---------------------------------------------------------------------  
    sys.exit()

######################################################################################################---Message Extracting Function

##############################################################################################################################
# Choose to embed a message or to extract a message

wel= raw_input('Welcom... \ninput h for hiding a message \nor e to extract a message\nq to quit the program:')

while wel != "q":

    if wel == "h" :
        hideMSG()

    if wel == "e":
        extractMSG()

    else:
        wel= raw_input('Welcom...please enter one of the following: \nh for hiding a message \nor e to extract a message\nq to quit the program:')
   

sys.exit()

##############################################################################################################################

