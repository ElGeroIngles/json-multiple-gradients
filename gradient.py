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
ifshowtext = False
ifshowitem = False
ifshowentity = False

# Ask to account for the changes made to JSONs in 1.21.5 (see "https://misode.github.io/versions/?id=1.21.5&tab=changelog&tags=breaking|text")
if input("Use 1.21.5+ JSON format? [Y/n] ").lower() == "n":
    new_format: bool = False

    # Changes to key and items in JSONs
    key_comma: str = '"'
    item_comma: str = '"'

    # Changes to text components names
    hover_event_key: str = "hoverEvent"
    click_event_key: str = "clickEvent"

    # Changes to text components args
    open_url_arg: str = "value"
    run_command_arg: str = "value"
    suggest_command_arg: str = "value"
    change_page_arg: str = "value"

    show_text_arg: str = "contents"
    show_item_arg: str = "value"
    show_entity_arg_uuid: str = "id"
    show_entity_arg_type: str = "type"
else:
    new_format: bool = True

    # Changes to key and items in JSONs
    key_comma: str = ''
    item_comma: str = "'"

    # Changes to text components names
    hover_event_key: str = "hover_event"
    click_event_key: str = "click_event"

    # Changes to text components args
    open_url_arg: str = "url"
    run_command_arg: str = "command"
    suggest_command_arg: str = "command"
    change_page_arg: str = "page" # Must be possitive

    show_text_arg: str = "text"
    show_item_arg: str = "id"
    show_entity_arg_uuid: str = "uuid"
    show_entity_arg_type: str = "id"

# Gets text and colors as hex code. Can only accept two colors.
text = list(input("Text: "))
# print(text)
text_ = str(''.join(text))
# print(text_)

def ask_gradients():
    global gradients
    gradients = int(input("Number of colors for gradients: "))
    if gradients > len(text_):
        print("ERROR: The number of colors can't be greater than the number of letters the text has. Please, try again.")
        ask_gradients()
    if gradients <= 1:
        print("ERROR: The number of colors must be greater than 1 to form a gradient. Please, try again.")
        ask_gradients()
ask_gradients()

colors = []
# colors = ["#fc0303","#fce803","#03fc07","#03fcf0","#030bfc","#a903fc","#fc0303"]
x = 0

for x in range(gradients):
    # print(x)
    colors.append(hextorgb(input(f"Color {x+1} (hex): ")))
    # print(colors[x])
    x =+ 1

# Sets decorator variables. If any of these return ANYTHING other than "true", it assumes they're false.
if input("Bold? [y/N] ").lower() == "y":
    bold = True
if input("Underline? [y/N] ").lower() == "y":
    underline = True
if input("Italics? [y/N] ").lower() == "y":
    italics = True
if input("Strikethrough? [y/N] ").lower() == "y":
    strikethrough = True
if input("Obfuscated? [y/N] ").lower() == "y":
    obfuscated = True
if input("Custom Font? [y/N] ").lower() == "y":
    custom_font = True
    font = input("Font: ")
if input("Click Event? [y/N] ").lower() == "y":
    def ask_click_event():
        try:
            click_event = int(input("Please, select one of the following:\n[0] Url\n[1] Run Command\n[2] Suggest Command\n[3] Copy to Clipboard\n[4] Change Page (Books Only)\n"))
        except:
            print("ERROR: Invalid selection. Please choose a number between 0 and 4. Please, try again.")
            ask_click_event()
        if click_event == 0:
            global ifurl
            global url
            ifurl = True
            url = input("Url: ")
        elif click_event == 1:
            global ifruncmd
            global command
            ifruncmd = True
            command = input("Command to run: ")
        elif click_event == 2:
            global ifsugcmd
            global sugcmd
            ifsugcmd = True
            sugcmd = input("Command to suggest: ")
        elif click_event == 3:
            global ifcopy
            global copy
            ifcopy = True
            copy = input("Text to copy: ")
        elif click_event == 4:
            global ifchgpage
            global chgpage
            ifchgpage = True
            chgpage = input("Change to page: ")
        else:
            print("ERROR: Invalid selection. Please choose a number between 0 and 4. Please, try again.")
            ask_click_event()
        return click_event
    click_event = ask_click_event()
if input("Hover Event? [y/N] ").lower() == "y":
    def ask_hover_event():
        try:
            hover_event = int(input("Please, select one of the following:\n[0] Show Text\n[1] Show Item\n[2] Show Entity"))
        except:
            print("ERROR: Invalid selection. Please choose a number between 0 and 2. Please, try again.")
            ask_hover_event()
        if hover_event == 0:
            global ifshowtext
            global showtext
            ifshowtext = True
            showtext = input("Text: ")
        elif hover_event == 1:
            global ifshowitem
            global showitem
            ifshowitem = True
            showitem = input("Item: ")
        elif hover_event == 2:
            global ifshowentity
            global showentity
            ifshowentity = True
            showentity = input("Entity: ")
        else:
            print("ERROR: Invalid selection. Please choose a number between 0 and 2. Please, try again.")
            ask_hover_event()
        return hover_event
    # hover_event = ask_hover_event()

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
divided_text = []
if gradients == 2:
    divided_text.append(text_)
else:
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
        doBold = f'{key_comma}bold{key_comma}:true,'
    else:
        doBold = ""

    if italics == True:
        doItalics = f'{key_comma}italic{key_comma}:true,'
    else:
        doItalics = ""

    if underline == True:
        doUnderline = f'{key_comma}underlined{key_comma}:true,'
    else:
        doUnderline = ""
        
    if ifurl == True:
        # doClickEvent = f'"clickEvent":{"action":"open_url","value":"{url}"},'
        doClickEvent = f'{key_comma}{click_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}open_url{item_comma},{key_comma}{open_url_arg}{key_comma}:{item_comma}{url}{item_comma}}},'
    
    if ifruncmd == True:
        # doClickEvent = f'"clickEvent":{"action":"run_command","value":"{command}"},'
        doClickEvent = f'{key_comma}{click_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}run_command{item_comma},{key_comma}{run_command_arg}{key_comma}:{item_comma}{command}{item_comma}}},'
    
    if ifsugcmd == True:
        # doClickEvent = f'"clickEvent":{"action":"suggest_command","value":"{sugcmd}"},'
        doClickEvent = f'{key_comma}{click_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}suggest_command{item_comma},{key_comma}{suggest_command_arg}{key_comma}:{item_comma}{sugcmd}{item_comma}}},'
        
    if ifcopy == True:
        # doClickEvent = f'"clickEvent":{"action":"copy_to_clipboard","value":"{copy}"},'
        doClickEvent = f'{key_comma}{click_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}copy_to_clipboard{item_comma},{key_comma}value{key_comma}:{item_comma}{copy}{item_comma}}},'

            
    if ifchgpage == True:
        # doClickEvent = f'"clickEvent":{"action":"change_page","value":"{chgpage}"},'
        doClickEvent = f'{key_comma}{click_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}change_page{item_comma},{key_comma}{change_page_arg}{key_comma}:{item_comma}{chgpage}{item_comma}}},'

    if ifshowtext == True:
        # doClickEvent = f'"clickEvent":{"action":"change_page","value":"{chgpage}"},'
        doClickEvent = f'{key_comma}{hover_event_key}{key_comma}:{{{key_comma}action{key_comma}:{item_comma}show_text{item_comma},{key_comma}{change_page_arg}{key_comma}:{item_comma}{chgpage}{item_comma}}},'

    if strikethrough == True:
        doStrikethrough = f'{key_comma}strikethrough{key_comma}:true,'
    else:
        doStrikethrough = ""

    if obfuscated == True:
        doObfuscated = f'{key_comma}obfuscated{key_comma}:true,'
    else:
        doObfuscated = ""

    if custom_font == True:
        doCustomFont = f'{key_comma}font{key_comma}:{item_comma}{font}{item_comma},'
    else:
        doCustomFont = ""

    # The main beast. Generates an individual json item for each character in string:text then slaps it onto the end of the final string.
        # print(text[i])
    final = final + f'{{{key_comma}text{key_comma}:{item_comma}{text[i]}{item_comma},{doBold}{doItalics}{doUnderline}{doObfuscated}{doCustomFont}{doStrikethrough}{doClickEvent}{key_comma}color{key_comma}:{item_comma}#{hexes[i]}{item_comma}}}'
    # If this is the last character, don't add a comma. Otherwise, do!
    if i != len(hexes) - 1:
        final = final + ','
# Finish off the json string.
final = final + ']'

# Print it out for the user to copy and use as fit.
print(final)
