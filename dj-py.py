from pygame import mixer
import pygame
import os
from os import listdir
from os.path import isdir, isfile, exists
from string import lower

global songs
songs = []

global result
result = []

global path
path = ""

global PAGE_LENGTH
PAGE_LENGTH = 25

def printHello () :
    print "\n*****             DJ - Py             *****"
    print "/                                         /"
    print "/                   by                    /"
    print "/                                         /"
    print "/             Giacomo Pinardi             /"
    print "/                                         /"
    print "/                 (2015)                  /"
    print "/                                         /"
    print "***** github.com/GiacomoPinardi/dj-py *****\n"
	
def printHelp () :
    print "github.com/GiacomoPinardi/dj-py"
    print "\n[init <path>]\n\tInit the folder with sound file\n\t<path> is the path's folder"
    print "\n[h], [help]\n\tPrint the help page"
    print "\n[quit]\n\tExit, return to shell"
    print "\n[pause], [stop]\n\tPause the current song"
    print "\n[play], [start]\n\tPlay the song previously paused"
    print "\n[pl]\n\tChange song/page number"
    print "\n[<page>:<text>]\n\tDisplay <page>th page of song with <text> in filename\n\t<page> number of sound found\n\t\tIf empty the first page is displayed\n\t<text> search song by text\n\t\tIf empty all files that contains '.' are displayed"

def initFolder (p):
    global path
    path = p
    try :
        if (path[len(path)-1] != "/"):
            path = path + "/"

        if (os.path.isdir(path)):
            all_things = listdir(path)
            del songs[:]
            for element in all_things:
                if (os.path.isfile(path + element)):
                    songs.append(element)
            if (len(songs) != 0):
                print "Successfull! [" + str(len(songs)) + "]"
        else:
            if (not os.path.exists(path)):
                print path + " doesn't exist!"
            else:
                print path + " is not a directory!"
            
    except OSError:
        print "Error: Permisson Denied!"

def view (page):
    global PAGE_LENGTH
    global songs
    pg = PAGE_LENGTH
    start = (pg * (page - 1))
    if (len(result) >= (pg * page)):
        pg = pg - 1   
        end = (pg * page) + 1
    elif ((len(result) < (pg * page)) and (len(result) > (pg * (page - 1)))):
        end = (len(result) % pg) + (pg * (page - 1))
    else:
        print "Error: Not Enough Song!"
        if (len(songs) == 0):
            print "Should first [init<path>]"

        end = 0

    for x in range(start, end):
        print "[" + str(x) + "]: " + result[x]

def listContains (data, page):
	global songs
	global result
	del result[:]
	for s in songs:
		lo = lower(s)
		if (lo.find(lower(data)) != -1):
			result.append(s)
	view(page)
	print ""

def playSong (songNumber):
    try :
	    mixer.music.load(path + result[songNumber])
	    mixer.music.play()
    except pygame.error:
        print "Error: Not A Song!\n"

def p_pSong (bool):
	if bool:
		mixer.music.unpause()
	else:
		mixer.music.pause()

def search (c):
    points = c.find(":")
    if (points == 0):
        page = 1
    else :                    
        page = int(c[:points])

    if (c[points+1] == " "):
        listContains(c[points+2:], page)
    else:
        listContains(c[points+1:], page)

def loop () :
    global PAGE_LENGTH
    quit = False
    while (not quit) :
        c = raw_input("\nCommand: ")	
        if (c == "" or c == "help" or c == "h"):
            printHelp();
        elif (c == "quit"):
            quit = True
        elif ((c[:4] == "init") and (len(c) > 5)):   
            initFolder(c[5:])
        elif (c == "pause" or c == "stop"):
            p_pSong(False)
        elif (c == "start" or c == "play"):
            p_pSong(True)
        elif (c == "pl"):
            try:
                newLength = int(raw_input("New Page Length: "))
                PAGE_LENGTH = newLength
            except ValueError:
                print "Error: Page Length Must Be a Number!"
        elif (c.find(":") != -1):            
            try:
                if (c.find(":") == (len(c)-1)):
                    if (len(c) == 1):
                        listContains(".", 1)
                    else:
                        listContains(".", int(c[:c.find(":")]))
                else:        
                    search(c)

                exit = False
                while (not exit):
                    number = raw_input("Song number: ")
                    if (number == "q"):
                        exit = True
                    elif (number.find(":") != -1) :
                        search(number)
                    elif (int(number) < len(result)):
                        playSong(int(number))
                    else:
                        print "Error: Max number: " + str(len(result) - 1)

            except ValueError:
                print "Error: Please only number as page/index!"
            except IndexError:
                print "Error: Please only number as page/index!"
        else:
            print "Type [h] for help page." 

# Main:
printHello()
mixer.init()
loop()
#