#!/usr/bin/python
#coding=utf-8

from uyr import uyr_hide
from uyr import uyr_extract
import argparse
import sys

def banner():
    print """
#####################################################################################
# _____         _              __ __                   _____         _              #
# |  |  | ___  _| | ___  ___   |  |  | ___  _ _  ___   | __  | ___  _| | ___  ___   #
# |  |  ||   || . || -_||  _|  |_   _|| . || | ||  _|  |    -|| .'|| . || .'||  _|  #
# |_____||_|_||___||___||_|      |_|  |___||___||_|    |__|__||__,||___||__,||_|    #
#                                                                                   #
#####################################################################################
#                                                                                   #"
#   UYR is an exfiltration and covert channel application                           #"
#   (1) Communicate with your friend in a stealthy manner                           #"
#   (2) Exfiltrate some data out of a network in control                            #"
#                                                                                   #"
#####################################################################################
\n"""

def Main():
    #banner()

    parser = argparse.ArgumentParser(description='Welcome to Under Your Radar (UYR)')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-e', "--extract", help="Extract Message from image", action="store_true")
    group.add_argument('-m', '--hide-msg', help="Hide Message in image", action="store_true")
    group.add_argument('-f', '--hide-file', help="Hide Text File in image", action="store")
    parser.add_argument('--image', help="Image file used to hide your message", action="store")
    parser.add_argument('--video', help="Video file used to hide your message", action="store")

    args = parser.parse_args()
    print parser.parse_args()

    path2Image = args.image
    path2Video = args.video

    if args.extract:
        uyr_extract.extractMSG(path2Image, path2Video)
    elif args.hide_msg:
        print "Performing operation: Hide Message"
        secretMessage = raw_input("Please enter your secret message: ")
        uyr_hide.hideMSG(secretMessage, path2Video, path2Image)
    elif args.hide_file:
        print "Performing operation: Hide Text File"
        hiddenFileName = args.hide_file
        with open(hiddenFileName, 'r') as hiddenFile:
            secretData = hiddenFile.read().strip('\n\r')
        uyr_hide.hideMSG(secretData, path2Video, path2Image)
    else:
        sys.exit()

if __name__ == '__main__':
    Main()

