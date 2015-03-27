#!/usr/bin/python
#coding=utf-8
__author__ = 'binary'

# Loading the required modules
import argparse
import sys
import os
#import zlib
from uyr import UYRLSB
from uyr import UYRStepic
from uyr import UYRUtils

version = '1.0'

def Main():
    print UYRUtils.uyr_banner()

    parser = argparse.ArgumentParser(description='Welcome to Under Your Radar (UYR)')
    parser.add_argument('-t', '--tweet', help="tweet your data", action="store", dest="tweet")
    parser.add_argument('-o', '--output', help='output file name', action="store", dest="output")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    hidegroup = parser.add_argument_group("hiding Operations")
    hgroup = hidegroup.add_mutually_exclusive_group()
    hgroup.add_argument('-m', '--hide-msg', help="hide message in image", action="store_true", dest="hmsg")
    hgroup.add_argument('-f', '--hide-file', help="hide text file in image", action="store", dest="htfile")
    hgroup.add_argument('-b', '--hide-bin', help="hide binary file in image", action="store", dest="hbfile")
    extractgroup = parser.add_argument_group("extracting Operations")
    egroup = extractgroup.add_mutually_exclusive_group()
    egroup.add_argument('-e', "--extract", help="extract message from image", action="store", dest="emsg")
    egroup.add_argument('-x', '--extract-bin', help="extract binary file from image", action="store", dest="ebfile")
    ivfgroup = parser.add_argument_group("image & video files to be used")
    ivfgroup.add_argument('--image', help="image file used for hiding", action="store", dest="image")
    ivfgroup.add_argument('--video', help="video file used for hiding/extracting", action="store", dest="video")
    args = parser.parse_args()
    #print parser.parse_args()
  
    if len(sys.argv) == 1:
       parser.print_help()

    # Doing some cleaning and checking:
    # Clearing the tmp directory before proceeding
    if os.path.exists('tmp'):
        UYRUtils.cleanTmpDir()

    # Prepare the tmp directory for processing
    UYRUtils.createTMPDir()

    # Message / Data Hiding
    if args.hmsg or args.htfile or args.hbfile:
        # Reading the Image and Video Files
        path2Image = args.image
        path2Video = args.video
        hideBinFile = args.hbfile
        hideTxTFile = args.htfile
        hideMsg = args.hmsg

        if not UYRUtils.checkPath2Image(path2Image):
            print "[+] Sorry image file does not exist"
            sys.exit()
        if not UYRUtils.checkPath2Video(path2Video):
            print "[+] Sorry video file does not exist"
            sys.exit()

        # Method to be performed on hiding a message
        if hideMsg:
            print "[+] Performing Operation: Hide Message"
            secretMessage = raw_input("[+] Enter your secret message: ")
            charmap = UYRLSB.hideMessage(secretMessage, path2Video, path2Image)
            print "[+] Hidden successfully!!!"
            print "[+] Your character map is: ", charmap

        # Method to be performed on hiding a txt file
        if hideTxTFile:
            print "[+] Performing Operation: Hide Text File"
            with open(hideTxTFile, 'r') as hiddenFile:
                secretData = hiddenFile.read().strip('\n\r')
            charmap = UYRLSB.hideMessage(secretData, path2Video, path2Image)
            print "[+] Hidden successfully!!!"
            print "[+] Your character map is: ", charmap

        # Method to be performed to hide a binary file
        if hideBinFile:
            print "[+] Performing Operation: Hiding Binary File"
            f = open(hideBinFile, 'rb')
            binaryContent = f.read()
            f.close()
            #zipSecretMessage = zlib.compress(binaryContent)
            #imgNamePNG = UYRStepic.hideMessage(zipSecretMessage, path2Video, path2Image)
            charmap = UYRStepic.hideMessage(binaryContent, path2Video, path2Image)
            print "[+] Hidden successfully!!!"
            print "[+] Your character map is: ", charmap

    # Message / Data Extraction
    if args.emsg or args.ebfile:
        path2Video = args.video
        extractMsg = args.emsg
        extractBinFile = args.ebfile

        # Method to be performed on message extraction
        if extractMsg:
            path2Image = args.emsg
            print "[+] Performing Operation: Extract Message"
            secMessage = UYRLSB.extractMSG(path2Image, path2Video)
            print "[+] Message extracted successfully!!!"
            print "[+] The secret message is: ", secMessage

        # Method to be performed to extract a binary file
        if extractBinFile:
            fName = args.output
            if not args.output:
                print "[+] Sorry you must provide a name for the output file!"
                sys.exit()

            path2Image = args.ebfile
            print "[+] Performing Operation: Extract Binary File"
            f2 = open(fName, 'wb+')
            #zippedBinaryData = UYRStepic.extractMSG(path2Image, path2Video)
            binaryFile = UYRStepic.extractMSG(path2Image, path2Video)
            #binaryFile = zlib.decompress(zippedBinaryData)
            #f2.write(zippedBinaryData)
            f2.write(binaryFile)
            f2.close()
            print "[+] Data extracted successfully!!!"
            print "[+] Extracted file named: %s" % fName
            print "[+] The binary file is: ", len(binaryFile), "bytes long"

    # Sending charmaps as tweets :)
    if args.tweet:
        txtTweet = unicode(raw_input("[+] Enter the required tweet message: "))
        print "[+] Caution: max file size twitter can handle is 5Mb"
        path2TweetImage = args.tweet

        configParser = UYRUtils.loadConfigFile('socialnetworks.ini')
        twitterInfo = UYRUtils.loadTwitterConfig(configParser)
        UYRUtils.tweetWithImage(twitterInfo, txtTweet, path2TweetImage)
        print "[+] Tweet sent successfully!!!"

    # Cleaning and exiting
    UYRUtils.cleanTmpDir()
    print "[+] UYR Finished Successfully!!!"
    sys.exit()

if __name__ == '__main__':
    Main()
