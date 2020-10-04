from time import sleep
import netifaces
import curses, os #curses is the interface for capturing key presses on the menu, os launches the files
screen = curses.initscr() #initializes a new window for capturing key presses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() # Lets you use colors when highlighting selected menu option
screen.keypad(1) # Capture input from keypad

# Change this to use different colors when highlighting
curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option
curses.curs_set(0)

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
INTSEL = "INTSEL" #select interface
WIFISEL = "WIFISEL" #used to generat wifi target list
WIFIOPT = "WIFIOPT" #select wifi target

wifilist = []
interfaces = netifaces.interfaces()

selected_interface = ""
interface_mode = ""
target = ""

list2 = []

for x in interfaces:
    list2.append({ 'title': x, 'type': INTSEL, 'command': x })
#crates an empty menu data
menu_data = {}
#function to set the data of the menu, called everytime data changes
def set_data():
    global menu_data
    menu_data = {
        'title': "Wicrack MX", 'type': MENU, 'subtitle': "selected interface: " + selected_interface + " interface mode: " + interface_mode + " target: " + target,
  	'options':[
        	{ 'title': "select network interface", 'type': MENU, 'subtitle': "selected interface: " + selected_interface,
        	'options': list2
        	},
        	{ 'title': "put interface in monitor mode", 'type': COMMAND, 'command': 'sudo airmon-ng start ' + selected_interface },
        	{ 'title': "put interface in managed mode", 'type': COMMAND, 'command': 'sudo airmon-ng stop ' + selected_interface +'mon' },
		{ 'title': "Fix network issues", 'type': COMMAND, 'command': 'sudo airmon-ng check kill \n sudo service NetworkManager restart' },
		{ 'title': "select Wifi target", 'type': WIFISEL, 'subtitle': "selected tarjet: " + target,
        'options': wifilist
        },
        	{ 'title': "DOS atack menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': COMMAND, 'command': 'echo > log funciona' },

        	]
        	},
		{ 'title': "Handshake/PMKID tools menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},
		{ 'title': "offline WPA/WPA2 cracking menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},
		{ 'title': "Evil Twin attack menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},
		{ 'title': "WPS attack menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},
		{ 'title': "WEP attack menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},
		{ 'title': "Enterprise attack menu", 'type': MENU, 'subtitle': "DOS attak menu",
        	'options': [
          	{'title': "NO", 'type': EXITMENU, },

        	]
        	},

  	]
	}

set_data()

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):
  global menu_data
  # work out what text to display as the last menu option
  if parent is None:
    set_data()
    menu = menu_data
    #os.system('echo > log menu principal')
    lastoption = "Exit"
  else:
    lastoption = "Return to %s menu" % parent['title']

  optioncount = len(menu['options']) # how many options in this menu

  pos = 0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
  oldpos = None # used to prevent the screen being redrawn every time
  x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program

  # Loop until return key is pressed
  while x != ord('\n'):
    if pos != oldpos:
      oldpos = pos
      screen.border(0)
      screen.addstr(2,2, menu['title'], curses.A_STANDOUT) # Title for this menu
      screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu


      # Display all the menu items, showing the 'pos' item highlighted
      for index in range(optioncount):
        textstyle = n
        if pos == index:
          textstyle = h
        screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
      # Now display Exit/Return at bottom of menu
      textstyle = n
      if pos == optioncount:
        textstyle = h
      screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
      screen.refresh()
      # finished updating screen

    x = screen.getch() # Gets user input

    # What is user input?
    if x >= ord('1') and x <= ord(chr(optioncount+1)):
      pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
    elif x == 258: # down arrow
      if pos < optioncount:
        pos += 1
      else: pos = 0
    elif x == 259: # up arrow
      if pos > 0:
        pos += -1
      else: pos = optioncount

  # return index of the selected item
  return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent = None):
  global selected_interface
  global interface_mode
  global target
  global menu_data
  global wifilist

  optioncount = len(menu['options'])
  exitmenu = False
  if parent is None:
       set_data()
       menu = menu_data

  while not exitmenu: #Loop until the user exits the menu
    getin = runmenu(menu, parent)
    if getin == optioncount:
        exitmenu = True

    elif menu['options'][getin]['type'] == COMMAND:
      #menu = menu_data
      curses.def_prog_mode()    # save curent curses environment
      os.system('reset')
      screen.clear() #clears previous screen
      os.system(menu_data['options'][getin]['command']) # run the command
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
      os.system('echo > log ' + str(menu))

    elif menu['options'][getin]['type'] == MENU:
        screen.clear() #clears previous screen on key press and updates display based on pos
        menu = menu_data
        processmenu(menu['options'][getin], menu) # display the submenu
        screen.clear() #clears previous screen on key press and updates display based on pos

    elif menu['options'][getin]['type'] == WIFISEL:
        wifi = os.system('nmcli dev wifi')
        for x in wifi:
            wifilist.append({ 'title': x, 'type': WIFIOPT, 'command': x })
        screen.clear() #clears previous screen on key press and updates display based on pos
        menu = menu_data
        processmenu(menu['options'][getin], menu) # display the submenu
        screen.clear() #clears previous screen on key press and updates display based on pos


    elif menu['options'][getin]['type'] == INTSEL:
        selected_interface = menu['options'][getin]['command']
        set_data()
        exitmenu = True #returns to main menu
        screen.clear()
        screen.refresh()
        os.system('echo > log ' + str(menu))

    elif menu['options'][getin]['type'] == EXITMENU:
        exitmenu = True

# Main program
processmenu(menu_data)
curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')