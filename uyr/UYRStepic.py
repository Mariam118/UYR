__author__ = 'binary'
#coding=utf-8

# Note:
# All code below needs improvement!

import sys
import shutil
import UYRUtils

try:
    import stepic
except ImportError:
    print "Hide Module: Sorry module python-stepic not found"

try:
    import Image
except ImportError:
    print "Hide Module: Sorry module python-pil not found"

try:
    import cv2
except ImportError:
    print "Hide Module: Sorry cv2 module not found"

try:
    import cv2.cv as cv
except ImportError:
    print "Hide Module: Sorry module cv2.cv not found"


positionList = []
###########################################################################################
# Function to search for char in frame
###########################################################################################
def foundChar(msgC, Fnum):
    k = 0
    imageFile = "tmp/frame%d.jpg" % Fnum

    fh = UYRUtils.hOpenImgBinary(imageFile)
    data = UYRUtils.readImgContent(fh)

    Num = ord(msgC)
    hexNum = hex(Num)[2:]
    for ch in data:
        # make a hex byte
        byt = "%02X" % ord(ch)
        if ord(ch) == Num:
            loc = k
            positionList.append((Fnum + k, ","))  # should remove byte
            return True
        k = k+1
    positionList.append((-1, ","))  # if the frame doesn't contain the identical value, add -1 to skip it
    #print positionList
    return False


#######################################################################################################
# Message Hiding Function #
######################################################################################################
def hideMessage(secretMessage, path2Video, path2Image, msgLength=0):
    # Read Video and check if video frame number is enough
    enoughSize = True

    while enoughSize:       # extracting frames
        vidcap = cv2.VideoCapture(path2Video)                        #print ("success")
    
        frameNumbers = vidcap.get(cv.CV_CAP_PROP_FRAME_COUNT)     #print ( frameNumbers )
        fps = vidcap.get(cv.CV_CAP_PROP_FPS)                    #print ( fps )
        videoLength = frameNumbers / fps    # seconds             #print ( videoLength )

        count = 0

        if videoLength < (msgLength / (fps*2)):
            print ("Sorry!!! not enough space to embed the message, try another video (more time)")
            n= raw_input('press n to try another video or any other key to exit:')
            if n != "n":
                sys.exit()
        else:
            # extracting frames
            enoughSize = False
            success, image = vidcap.read()
            while success:
                success, image = vidcap.read()
                cv2.imwrite("tmp/frame%d.jpg" % count, image)     # save frame as JPEG file
                count += 1

    #split msg char, search and create positions for chars
    msgList = list(secretMessage)
    c = 0

    found = False #infinite loop here
    for msgChar in msgList:
        while not(found):
            found = foundChar(msgChar, c)
            c = (c+1) % count
        found = False

    # Write positions list to a text file
    tmpFile = open("tmp/tmpFile.txt", "w")
    tmpFile.write('\n'.join('%s %s' % x for x in positionList))
    tmpFile.close()

    # read from file and save in string
    dataEm =""
    for line in open("tmp/tmpFile.txt"):
        words = line.strip().split(',')
        dataEm = dataEm + " " + words[0]
        dataEm = dataEm + "\n"

    pathList = path2Image.split("/")
    imgNameJPG = pathList[-1]
    imgName = imgNameJPG.split(".")

    #print "this is the data to be hidden: \n", dataEm
    carrier = Image.open(path2Image)
    stegoIM2 = stepic.encode(carrier, dataEm)
    #stegoIM2.save('./charmap.png', 'PNG')

    imgNamePNG = imgName[0]+".png"
    stegoIM2.save(imgNamePNG, 'PNG')
    #print "[+] {0:<50} [+]".format("./charmap.png is the character map (from fun)")
    return imgNamePNG


######################################################################################################
# Message Extracting Function
######################################################################################################
def extractMSG(path2Image, path2Video):
    # Extract from picture
    im = Image.open(path2Image)
    s = stepic.decode(im)

    tmpFile = open("tmp/PositionsList.txt", "w")
    tmpFile.write(s)
    tmpFile.close()

    #Read Video file frames
    absPath = path2Video
    vidcap = cv2.VideoCapture(absPath)

    count = 0
    success, image = vidcap.read()
    while success:
        success, image = vidcap.read()
        cv2.imwrite("tmp/frame%d.jpg" % count, image)     # save frame as JPEG file
        count += 1

    # extract message from frames
    fNum = 0
    secMSG = ""
    for line in open("tmp/PositionsList.txt"):
        word = int(line.strip())
        #print "The word is now: ", word
        if word != -1:
            cPos = word - fNum
            imgName = "tmp/frame%d.jpg" % fNum
            try:
                imageFile = imgName
                data = open(imageFile, "rb").read()
            except IOError:
                print "Image file %s not found" % imageFile
                raise SystemExit

            msgOrd = data[cPos]
            secMSG = secMSG + msgOrd
        fNum = (fNum + 1) % count

    #shutil.rmtree('tmp')
    return secMSG

