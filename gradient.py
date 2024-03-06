# NOT CREATED BY ME (ElGeroIngles), THIS GENERATOR BELONGS TO rackodo (https://github.com/rackodo/gradient-json-minecraft) AND HAS BEEN MODIFIED TO SUPPORT MORE FEATURES

# Minecraft JSON gradient generator. If you use this script in any of your personal projects, please credit me and link the original repository (https://github.com/rackodo/gradient-json-minecraft), no need to credit the modified repository.
# Script by Bash Elliott and modified by ElGeroIngles.

import numpy as np

# Hex to RGB and RGB to Hex functions by Sachin Rastogi. 
# https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/

def hextorgb(hex_color):
    # print(hex_color)
    hex_color = hex_color.lstrip('#')
    return(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

def rgbtohex(rgb):
    return '%02x%02x%02x' % rgb

def split(word):
    return list(word)

# Initialize decorator variables.
bold = False
underline = False
italics = False
ifurl = False
ifruncmd = False
ifchgpage = False
ifcopy = False
ifsugcmd = False
strikethrough = False
obfuscated = False
custom_font = False

# Gets text and colors as hex code. Can only accept two colors.
text = list(input("Text: "))
# print(text)
text_ = str(''.join(text))
# print(text_)

def ask_gradients():
    global gradients
    gradients = int(input("How many gradients: "))
    if gradients > len(text_):
        print("The number of gradients can't be more than the number of letters the text has.")
        ask_gradients()
    if gradients <= 1:
        print("The number of gradients must be greater than 1.")
        ask_gradients()
ask_gradients()

colors = []
# colors = ["#fc0303","#fce803","#03fc07","#03fcf0","#030bfc","#a903fc","#fc0303"]
x = 0

for x in range(gradients):
    # print(x)
    colors.append(hextorgb(input(f"Color {x+1}: ")))
    # print(colors[x])
    x =+ 1

# Sets decorator variables. If any of these return ANYTHING other than "true", it assumes they're false.
if input("Bold?: ").lower() == "true":
    bold = True
if input("Underline?: ").lower() == "true":
    underline = True
if input("Italics?: ").lower() == "true":
    italics = True
if input("Strikethrough?: ").lower() == "true":
    strikethrough = True
if input("Obfuscated?: ").lower() == "true":
    obfuscated = True
if input("Custom Font?: ").lower() == "true":
    custom_font = True
    font = input("Font: ")
if input("Click Event?: ").lower() == "true":
    def ask_click_event():
        try:
            click_event = int(input("Please, select one of the following:\n[0] Url.\n[1] Run Command.\n[2] Suggest Command.\n[3] Copy to Clipboard.\n[4] Change Page (Books Only).\n"))
        except:
            print("Invalid selection. Please choose a number between 0 and 4.")
            ask_click_event()
        if click_event == 0:
            global ifurl
            global url
            ifurl = True
            url = input("Link: ")
        elif click_event == 1:
            global ifruncmd
            global command
            ifruncmd = True
            command = input("Command: ")
        elif click_event == 2:
            global ifsugcmd
            global sugcmd
            ifsugcmd = True
            sugcmd = input("Suggest: ")
        elif click_event == 3:
            global ifcopy
            global copy
            ifcopy = True
            copy = input("Copy: ")
        elif click_event == 4:
            global ifchgpage
            global chgpage
            ifchgpage = True
            chgpage = input("Page: ")
        else:
            print("Invalid selection. Please choose a number between 0 and 4.")
            ask_click_event()
        return click_event
    click_event = ask_click_event()

# Divide text in "equal" parts for each color gradient.
def divide_text(txt, num_parts):
    len_total = len(txt)
    len_part = len_total // num_parts
    # print(len_part)
    parts = []
    temp = []
    temp_ = ""
    _temp_ = ""

    start = 0
    for i in range(num_parts):
        end = start + len_part
        if i == num_parts - 1:
            # print("a")
            temp.append(txt[start:end])
            temp.append(txt[end:])
            i = 0
            j = 0
            # print(temp)
            while not temp[len(temp)-1] == "":
                # print("\nwhile\n")
                # print(f"i: {i}")
                # print(f"j: {j}")
                if i == 0:
                    for x in range(len(temp)):
                        # print(f"x: {x}")
                        try:
                            if not x+j+2 == len(temp):
                                temp[x+j] += temp[x+j+1][0]
                                temp[x+j+1] = temp[x+j+1][1:]
                        except:
                            # print("except")
                            pass
                    if j == len(temp)-1:
                        # print(f"if j: {j}")
                        j = 0
                    else:
                        # print(f"j + 1: {j+1}")
                        j += 1
                        i += 1
                else:
                    temp[len(temp)-2] += temp[len(temp)-1][0]
                    temp[len(temp)-1] = temp[len(temp)-1][1:]
                    i = 0
                # print(f"result: {temp}")
            temp.pop()
                
        else:
            # print("b")
            temp.append(txt[start:end])
        start = end
    # return temp

    for i in range(len(temp)-1):
        temp_ = temp[i]
        if i == len(temp)-2:
            _temp_ = temp_[int(len(temp_)/2):]
            _temp_ += temp[i+1]
            parts.append(_temp_)
        else:
            if i == 0:
                _temp_ = temp_[0:]
            else:
                _temp_ = temp_[int(len(temp_)/2):]

            try:
                temp_ = temp[i+1]
                _temp_ += temp_[:int(len(temp_)/2)]
                parts.append(_temp_)
            except:
                pass

    return parts
divided_text = divide_text(text_, gradients)
# print(divided_text)

# Setup the gradients:
def gradient(n):
    # print(n)
    global numPoints
    global points
    global hexes

    # Sets the number of RGB values to make in the following array.
    if not n+1 == len(divided_text):
        divided_text[n] = divided_text[n] + divided_text[n+1][0]
    numPoints = len(divided_text[n])

    color_start = colors[n]
    color_end = colors[n+1]

    # Create an equal space array of RGB values ​​between color_start and color_end inclusive.
    points = np.linspace(color_start, color_end, numPoints, dtype=int)

    # Initializes array:hexes, then sets the array to array:points, ~hexified~.
    for i in range(len(points)):
        hexes.append((rgbtohex(tuple(points[i]))))

    if not n+1 == len(divided_text):
        hexes.pop()

    if not n+1 >= len(divided_text):
        n += 1
        # print(hexes)
        # print(n)
        gradient(n)
hexes = []
gradient(0)

# This mess generates the final text.
final = '["",'
# print(f"hexes: {hexes}")
for i in range(len(hexes)):
    doBold = ""
    doUnderline = ""
    doItalics = ""
    doUrl = ""
    doClickEvent = ""
    doStrikethrough = ""
    doObfuscated = ""
    doCustomFont = ""

    # Sets the strings to be used if the user sets their respective decorator variables to be true.
    if bold == True:
        doBold = '"bold":true,'
    else:
        doBold = ""

    if italics == True:
        doItalics = '"italic":true,'
    else:
        doItalics = ""

    if underline == True:
        doUnderline = '"underlined":true,'
    else:
        doUnderline = ""
        
    if ifurl == True:
        doClickEvent = '"clickEvent":{"action":"open_url","value":"'
        doClickEvent += f'{url}'
        doClickEvent += '"},'

    if ifruncmd == True:
        doClickEvent = '"clickEvent":{"action":"run_command","value":"'
        doClickEvent += f'{command}'
        doClickEvent += '"},'
    
    if ifsugcmd == True:
        doClickEvent = '"clickEvent":{"action":"suggest_command","value":"'
        doClickEvent += f'{sugcmd}'
        doClickEvent += '"},'
        
    if ifcopy == True:
        doClickEvent = '"clickEvent":{"action":"copy_to_clipboard","value":"'
        doClickEvent += f'{copy}'
        doClickEvent += '"},'

            
    if ifchgpage == True:
        doClickEvent = '"clickEvent":{"action":"change_page","value":"'
        doClickEvent += f'{chgpage}'
        doClickEvent += '"},'

    if strikethrough == True:
        doStrikethrough = '"strikethrough":true,'
    else:
        doStrikethrough = ""

    if obfuscated == True:
        doObfuscated = '"obfuscated":true,'
    else:
        doObfuscated = ""

    if custom_font == True:
        doCustomFont = f'"font":"{font}",'
    else:
        doCustomFont = ""

    # The main beast. Generates an individual json item for each character in string:text then slaps it onto the end of the final string.
        # print(text[i])
    final = final + '{{"text":"{}",{}{}{}{}{}{}{}"color":"#{}"}}'.format(text[i], doBold, doItalics, doUnderline, doObfuscated, doCustomFont, doStrikethrough, doClickEvent, hexes[i])
    # If this is the last character, don't add a comma. Otherwise, do!
    if i != len(hexes) - 1:
        final = final + ','
# Finish off the json string.
final = final + ']'

# Print it out for the user to copy and use as fit.
print(final)
