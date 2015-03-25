__author__ = 'binary'
import os
import shutil
import twitter
import ConfigParser

# Loading the required modules
try:
    from LSBSteg import LSBSteg
except ImportError:
    print "Hide Module: Sorry module LSBSteg not found"

try:
    import cv2
except ImportError:
    print "Hide Module: Sorry cv2 module not found"

try:
    import cv2.cv as cv
except ImportError:
    print "Hide Module: Sorry module cv2.cv not found"

def hOpenImgBinary(imgfileName):
    '''Open an Image file in binary mode and return the handler'''
    try:
        fHandler = open(imgfileName, "rb")
        return fHandler
    except IOError:
        #raise "Image file %s not found" % imageFile
        raise SystemExit

def readImgContent(fHandler):
    '''Read the Image file content'''
    try:
        imgContentData = fHandler.read()
        return imgContentData
    except IOError:
        #raise "Wrong Image File Handler"
        raise SystemExit

def calcMSGLength(secretMessage, path2Video):
    '''Calculates the message length'''
    vidcap = cv2.VideoCapture(path2Video)
    frameNumbers = vidcap.get(cv.CV_CAP_PROP_FRAME_COUNT)
    fps = vidcap.get(cv.CV_CAP_PROP_FPS)
    videoLength = frameNumbers / fps   # seconds
    return videoLength

def hVideoCap(path2Video):
    '''Return handler to video file'''
    return cv2.VideoCapture(path2Video)

def createTMPDir():
    '''tmp directory creator'''
    os.mkdir('tmp')

def cleanTmpDir():
    '''tmp directory remover'''
    shutil.rmtree('tmp')

def checkPath2Image(path2Image):
    '''checks if the image given exists'''
    return os.path.exists(path2Image)

def checkPath2Video(path2Video):
    '''checks if the video given exists'''
    return os.path.exists(path2Video)

def loadConfigFile(configFName):
    '''Loads an ini configuration file'''
    hConParser = ConfigParser.SafeConfigParser()
    hConParser.read(configFName)
    return hConParser

def loadTwitterConfig(hConParser):
    '''Loads the twitter API keys'''
    conkey = hConParser.get('twitter', 'consumer_key')
    conscrt = hConParser.get('twitter', 'consumer_secret')
    atokey = hConParser.get('twitter', 'access_token_key')
    atokscrt = hConParser.get('twitter', 'access_token_secret')
    twitterInfo = [conkey, conscrt, atokey, atokscrt]
    return twitterInfo

def tweetWithImage(twitterInfo, txtTweet, path2TweetImage):
    '''Sends a tweet using the Twitter API'''
    consumer_key, consumer_secret, access_token_key, access_token_secret = twitterInfo
    api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
    api.PostMedia(txtTweet, path2TweetImage)

def uyr_banner():
    '''Prints under your radar banner, what else? :)'''
    return """#####################################################################################
#  _____         _              __ __                   _____         _             #
# |  |  | ___  _| | ___  ___   |  |  | ___  _ _  ___   | __  | ___  _| | ___  ___   #
# |  |  ||   || . || -_||  _|  |_   _|| . || | ||  _|  |    -|| .'|| . || .'||  _|  #
# |_____||_|_||___||___||_|      |_|  |___||___||_|    |__|__||__,||___||__,||_|    #
#                                                                                   #
#####################################################################################"""
