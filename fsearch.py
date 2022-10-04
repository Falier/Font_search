from cgitb import html
import sys
from bs4 import BeautifulSoup
import requests
import re
import os
from array import *

#!/bin/bash

def font_search(search) :

    URL = "https://www.1001fonts.com/search.html?search={}".format(search)

    START = """<ul class=font-list>"""
    END = "</ul>"

    Font_links = []
    Font_names = []
    Link_names = []

    data = requests.get(URL).text

    result = re.search('{}(.*){}'.format(START, END), data)
    Font_List = result.group(1)

    soup = BeautifulSoup(data, "lxml")

    i = 0
    for link in soup.find_all('a'):
        font_link = link.get('href')
        link_start = font_link[0:10:1]
        if link_start == "/download/" :
            complete_link = "https://www.1001fonts.com{}".format(font_link)
            Font_links.append(complete_link)
    
    for foo in soup.find_all('img', alt=True):
        if foo['alt'] != "1001 Fonts logo" :
            Font_names.append(foo['alt'])

    i=1
    for name in Font_links :
        continueLoop = True
        while continueLoop :
            s = name[-i:]
            s = s[:1]
            if s == '/' :
                Link_names.append(name[-i:])
                continueLoop = False
            i += 1
        i=1

    i = 0
    for name in Font_names:
        print("[{}]: {}".format(i + 1, Font_names[i]))
        i += 1



    continueLoop = True
    while(continueLoop) :
        font_input = input('Please choose a font: ')
        
        try:
            font_input = int(font_input)
        except ValueError:
            print('Please enter a valid number (1-10)')
 

        if type(font_input) == type(i) :
            if ((font_input > 0) and (font_input < 11)):
                font_input -= 1
                print("You choose the font: {}".format(Font_names[font_input]))
                print("Link: {}".format(Font_links[font_input]))
                File_name = Link_names[font_input].replace("/", "")
                os.system('cd && wget {}'.format(Font_links[font_input]))
                continueLoop = False
            else :
                print("Please enter a valid number (1-10)")

    os.system('cd && mkdir -p ~/.fonts')
    os.system('cd && mv {} ~/.fonts/'.format(File_name))
    os.system('cd ~/.fonts && unzip {} && rm {}'.format(File_name, File_name))


if __name__ == '__main__' :
    font_search("papa")
