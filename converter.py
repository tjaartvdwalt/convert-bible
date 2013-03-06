# -*- coding: utf-8 -*-
'''
    convert-bible.py: Downloads the Afrikaans Bible text from www.bybel.co.za 
    and converts it to a single html file.

    Copyright (C) 2011  Tjaart van der Walt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import xml.dom.minidom
import re
import codecs
import sys

from urllib import request

def bybelboeke():
    return (
("GEN", "Genesis", 50), ("EXO", "Eksodus",  40), ("LEV", "Levitikus",  27),
("NUM", "Numeri",  36), ("DEU", "Deuteronomium",  34), ("JOS", "Josua",  24),
("JDG", "Rigters",  21), ("RUT", "Rut",  4), ("1SA", "1 Samuel",  31), 
("2SA", "2 Samuel",  24), ("1KI", "1 Konings",  22), ("2KI", "2 Konings",  25),
("1CH", "1 Kronieke",  29), ("2CH", "2 Kronieke",  36), ("EZR", "Esra",  10),
("NEH", "Nehemia",  13), ("EST", "Ester", 10), ("JOB", "Job", 42),
("PSA", "Psalms", 150), ("PRO", "Spreuke", 31), ("ECC", "Prediker", 12),
("SNG", "Hooglied", 8), ("ISA", "Jesaja", 66), ("JER", "Jeremia", 52),
("LAM", "Klaagliedere", 5), ("EZK", "Esegiël", 48), ("DAN", "Daniël", 12),
("HOS", "Hosea", 14), ("JOL", "Joël", 3), ("AMO", "Amos", 9),
("OBA", "Obadja", 1), ("JON", "Jona", 4), ("MIC", "Miga", 7),
("NAM", "Nahum", 3), ("HAB", "Habakuk", 3), ("ZEP", "Sefanja", 3),
("HAG", "Haggai", 2), ("ZEC", "Sagaria", 14), ("MAL" , "Maleagi", 4),

("MAT", "Matteus", 28), ("MRK", "Markus", 16), ("LUK", "Lukas", 24),
("JHN", "Johannes", 21), ("ACT", "Handelinge", 28), ("ROM", "Romeine", 16), 
("1CO", "1 Korintiërs", 16), ("2CO", "2 Korintiërs", 13), 
("GAL", "Galasiërs", 6), ("EPH", "Efesiërs", 6), ("PHP", "Filippense", 4),
("COL", "Kolossense", 4), ("1TH", "1 Timoteus", 5), ("2TH", "2 Timoteus", 3),
("1TI", "1 Tessalonisense", 6), ("2TI", "2 Tessalonisense", 4),
("TIT", "Titus",3), ("PHM", "Filemon", 1), ("HEB", "Hebreërs", 13),
 ("JAS", "Jakobus", 5), ("1PE", "1 Petrus", 5), ("2PE", "2 Petrus", 3),
 ("1JN", "1 Johannes", 5), ("2JN", "2 Johannes", 1), ("3JN", "3 Johannes", 1),
 ("JUD", "Judas", 1), ("REV" , "Openbaring", 22)
)

def generateTOC(boeke):
    output = u"<a name=indeks><h1>Indeks</h1></a>"
    output += "<table>\n"
    for i in range(0, len(boeke)):
        (boekKort, boekLank, maxRange) = boeke[i]
        output += "<tr><td><a href=\"#" + boekKort + "\">" + boekLank + "</td></tr>\n"
    output += "</table>\n"
    return output

def generateBookIndex(boekKort, boekLank, maxRange):
    output = "<a name=\"" + boekKort + "\"><h1>" + boekLank + "</h1></a>\n"
    output += "<table>"
    output += "<tr><td><a href=\"#indeks\">Indeks</a></td></tr>\n"
    for j in range(1, maxRange + 1):
        output += "<tr><td><a href=\"#" + boekKort + str(j) + "\">" + boekLank + " " + str(j) + "</a></td></tr>"
    output += "</table>"
    return output

def parseChapter(chapterNumber, boekKort, boekLank):
    url = request.urlopen("http://bybel.co.za/search/search-detail.php?book=" + boekKort + "&chapter="+ str(chapterNumber) + "&version=1&GO=Wys").read().decode('utf-8')


    startPos = re.search("<table width=\"550\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" summary=\"Book Results\" id=\"book-results\">", url).start()

    endPos = re.search("<\/table>", url).end()
    url = url[:endPos]


    verse_en_voetnotas = re.findall("<td><p><p>(.*?)</p></p>(</td><td width=100><b>.*?</b>(.*?)</td>)*", url)

    output = "<a name=\"" + boekKort + str(chapterNumber) + "\"></a><h2><a href=\"#" + boekKort + "\">" + boekLank + "</a> " + str(chapterNumber) + "</h2>\n"
    vers_nr = 1
    voetnota_nr = 1
    voetnota_html = ""
    for (vers, garbage, voetnota) in verse_en_voetnotas:
        output += "<sup>" +str(vers_nr) + "</sup>\n"
        output += vers + "\n"
        vers_nr += 1
        if(voetnota != ""):
            reference = boekKort + str(chapterNumber) + "_" + str(voetnota_nr)
            reverse_reference = reference + "_rev"
            output += "<a name=\"" + reverse_reference + "\"><a href=\"#" + reference + "\"><sup>[" + chr(voetnota_nr + 96) + "]</sup></a></a>\n"
            voetnota_html += "<a name=\"" + reference + "\"><p><a href=\"#" + reverse_reference + "\"><sup>[" + chr(voetnota_nr + 96) + "]</sup></a>" + voetnota + "</a></p>\n"
            voetnota_nr += 1
    if(voetnota_html != ""):
        output +="<h3>Voetnotas</h3>" + voetnota_html
    return output

'''
This method puts it all together.
It iterates through all the books in the array, and iterates over every chapter.
It returns the entire book in pretty html.
'''
def getDocument():
    boeke = bybelboeke()

    # start the html
    output = "<html>\n"
    # set the encoding
    output += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"

    #Create the table of contents
    output += generateTOC(boeke)

    # Iterate through all the books
    for i in range(0, len(boeke)):
        (boekKort, boekLank, maxRange) = boeke[i]
        print("Parsing: " + str(boekLank))

        # Generate the index for each book
        output += generateBookIndex(boekKort, boekLank, maxRange)

        # Iterate through all the chapters in the current book
        for j in range(1, maxRange + 1):
            # Download the current chapter from the web and format it properly
            output += parseChapter(j, boekKort, boekLank)

        # end the html
        output += "</html>"
    return output
def writeToFile(output, fileName):
    f = codecs.open(fileName, encoding='utf-8', mode='w+')
    f.write(output)
    f.close()

if __name__ == "__main__":
    # We use != 2 here, because the script name is the 1st argument
    if(len(sys.argv) != 2):
        print('This script takes the output file as a command line argument.')
        print("For example:\n" + sys.argv[0] + " bible.html")
        exit(1)
    output = getDocument()
    writeToFile(output, sys.argv[1])
