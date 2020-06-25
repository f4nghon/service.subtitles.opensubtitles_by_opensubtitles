# -*- coding: utf-8 -*-
# SRT files are only supported

import re
import io
from shutil import copyfile

timestamp_reg = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$")
linenum_reg = re.compile(r"^\d+$")

def addfontcolor(lines, color):
    output = []
    length = len(lines)
    for linenum in range(length):
        line = lines[linenum]
        if linenum_reg.match(line):
            # new sub line, next should be timestamp
            output.append(line + '\n')
            linenum += 1
            line = lines[linenum]
            if timestamp_reg.match(line):
                # timestamp, next line(s) are the subs
                output.append(line + '\n')
                linenum += 1
                line = lines[linenum]
                convertedline= "<font color=#" + color + ">"
                contains_font_color = False
                while not linenum_reg.match(line):
                    if line.startswith("<font color=#"):
                        contains_font_color = True
                        convertedline += line[line.index('>') + 1:] + '\n'
                    else:
                        convertedline += line + '\n'
                    linenum += 1
                    if(linenum >= length):
                        break
                    line = lines[linenum]
                if contains_font_color:
                    output.append(convertedline)
                else:
                    output.append(convertedline[:-2] + "</font>" + '\n\n')
                linenum += 1           
            else :
                print ("Unknown line: " + line + ", at line number: " + linenum)
                exit(3)
    return output

def clearfontcolor(lines):
    output = []
    for line in lines:
        if line.startswith("<font color=#"):
            output.append(line[line.index('>') + 1:].replace("</font>") + '\n')
        else:
            output.append(line.replace("</font>", "") + '\n')
    return output


def parsefile(filepath, fontcolor):
    # read file
    try:
        f = io.open(filepath, "r", encoding="utf8")
        lines = f.read().splitlines()
    except:
        print("UTF8 failed, trying CP1250...")
        try:
            f = io.open(filepath, "r", encoding="cp1250")
            lines = f.read().splitlines()
        except:
            print("Unknown file encoding...")
            return
    finally:
        f.close()

    output = []
    if(fontcolor == "FFFFFF"):
        output = clearfontcolor(lines)
    else:
        output = addfontcolor(lines, fontcolor)

    with io.open(filepath, 'w', encoding="utf8") as f:
        for item in output:
            f.write(item)