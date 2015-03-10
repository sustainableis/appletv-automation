#! /usr/bin/env python

import applescript
import subprocess
import os
import xml.etree.ElementTree as ET
import time
import datetime
import traceback
import urllib2

# def check_network():
    
#     #ping google DNS
#     devnull = open(os.devnull, "w")
#     status = subprocess.call(["ping", "-c", "1", "8.8.8.8"], 
#     	stdout=devnull, stderr=devnull)

#     if status == 0:
#         return True
#     else:
#         return False

def check_network():

    try:
        response=urllib2.urlopen('http://www.google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def connect_apple_tvs(appletv_dict):

	for pid in appletv_dict:
		scripts.call("connect_apple_tv", pid, appletv_dict[pid])
		time.sleep(2)
	return

def get_display_string():

	res = scripts.call("get_screen_coords")

	display_string = "Display 1 - (" + str(res[2]) + "x" + str(res[3]) + ")"

	return display_string


def kill_airparrots():

	subprocess.call(["killall", "AirParrot"])

	return

def get_appletv_names():

	displayprefs = u'Open Displays Preferences'
	projectorcal = u'Open Projector Calibrator'

	def passband(s):
 
		if (displayprefs in s):
			return False
		if (projectorcal in s):
			return False

		return True

	appletvs = []

	while True:
		try:
			# get appletv names, removing the last element in the list
			# because that's just a system menu name
			appletvs = scripts.call("find_appletv_names")

		except applescript.ScriptError:

			print "Applescript Error while getting appletv names!"
			print traceback.format_exc()

			# give a little time for the system to figure out whats up
			time.sleep(15)

			continue

		# no exception, break
		break

	# let the record show that i tried using filter() and 
	# a list comprehension. 
	appletvs_filtered = []

	for appletv in appletvs:
		if passband(unicode(appletv)):
			appletvs_filtered.append(appletv)

	return appletvs_filtered

def match_appletv_name(appletvs, target):

	# find the appletv name as reported by the OS
	# that contains the target name
	for appletv in appletvs:

		if target in appletv:
			return appletv

def mirror_display(appletvs, display):

	kill_airparrots();

	for appletv in appletvs:
		print "Spawning AirParrot for " + appletv + " on " + display
		# spawn an airparrot
		subprocess.call(["open", "-n", "/Applications/AirParrot.app"])
		#give it a second
		time.sleep(2)
		# mirror the display
		scripts.call("connect_single_apple_tv", appletv, display)
		time.sleep(5)

	return

def disable_screensaver():

	os.system('defaults -currentHost write com.apple.screensaver idleTime 0')


# this object will hold all of our applescript functions
# as one big string
scripts = applescript.AppleScript('''


	on display_dashboard(dashboard_url)
		tell application "Google Chrome"
			if it is running then
				quit
			end if
			
			activate
			delay 2
			open location dashboard_url
			activate
	
		end tell


	end display_dashboard 

	on toggle_presentation_mode()
		tell application "System Events" 
			keystroke "f" using {command down, shift down} 
		end tell
	end toggle_presentation_mode

	on get_screen_coords()
		tell application "Finder"
			set res to bounds of window of desktop

			return res
		end tell
	end get_screen_coords

	on disable_underscan()
		tell application "AirParrot"
			activate

			set underscan to 0

			set stretchApps to disabled

		end tell
	end disable_underscan

	on connect_single_apple_tv(appletv_name, display_name)
		tell application "AirParrot"
			activate
			repeat until device appletv_name exists
				count device
			end repeat

			if device appletv_name exists then
				set selectedDisplay to display named display_name 

				set connectedDevice to device named appletv_name

			end if



		end tell
	end connect_single_apple_tv
	
	on find_appletv_names()
		tell application "System Events"
			tell process "SystemUIServer"
				tell (menu bar item 1 of menu bar 1 whose description contains "Displays")
					click it
					
					set menuItems to menu items of menu 1
					
					set appletvs to {}
					
					repeat with menuItem in menuItems
						
						if value of attribute "AXEnabled" of menuItem is true then
							set end of appletvs to name of menuItem
						end if
						
					end repeat
					
					return appletvs
					
				end tell
				
			end tell
			
		end tell
end find_appletv_names

''')

print "******* SIS DASHBOARD AUTOMATION *********"

# ---------- Read config file ---------------

dashboard_url = ""
target_appletv = ""

#read config
with open("config.txt", "r") as f:
	#dashboard_url = f.readline().rstrip()
	target_appletv = f.readline().rstrip()

#print "Dashboard URL: " + dashboard_url
print "Target AppleTV: " + target_appletv

# attempt to get AppleTV names
#appletvs = get_appletv_names()



#print "OS reports the following AppleTVs: " + str(appletvs)

#get display name
#displayname = get_display_string()
displayname = "Display 1 - (1920x1080)"

print "Display string: " + displayname

if check_network():
    print "Network up!"
else:
	print "Network down!" 

print "Disabling screensaver.."
disable_screensaver()

print "Mirroring in 10 seconds.."

time.sleep(10)

# open chrome and display dashboard url
#scripts.call("display_dashboard", dashboard_url)

#time.sleep(4)

# connect apple tv, map target appletv to name reported by OS
print "Connecting target appletv " + target_appletv + "..."
#resolved_appletv = match_appletv_name(appletvs, target_appletv)
#print "Resolved appletv name: " + resolved_appletv 
#scripts.call("connect_single_apple_tv", resolved_appletv, displayname)
scripts.call("connect_single_apple_tv", target_appletv, displayname)

print "Disabling underscan in 10 seconds.."
time.sleep(10)

scripts.call("disable_underscan")



#print "Presentation mode in 10 seconds.."
#time.sleep(10)

# enter presentation mode on chrome
#scripts.call("toggle_presentation_mode")


# now we will loop forever, checking the network state.  if we 
# discover the network is down, we will wait for it to come back up and 
# and then reconnect all appletvs

# 0 = connected, 1 = disconnected
state = 0;

while True:

	if (check_network()):

		if (state == 1):
			# disconnected state, network is back up 
			# attempt to reconnect displays
			now = str(datetime.datetime.now())
			print now + ":Network up!\nAttempting to reconnect displays.."

			# get appletv names again, as they may have changed. 
			#appletvs = get_appletv_names()
			time.sleep(2)
			#scripts.call("connect_single_apple_tv", match_appletv_name(appletvs, target_appletv), displayname)
			scripts.call("connect_single_apple_tv", target_appletv, displayname)

			time.sleep(4)

			scripts.call("disable_underscan")
			state = 0;

	else:
		now = str(datetime.datetime.now())

		if (state == 0):
			# connected state, but the network went down
			# wait a shorter amount of time and then attempt
			# a reconnect.  If the network is still not up
			# the normal wait will apply. 

			print now + ": Network down\nAttempting reconnect in 20 seconds.."
			state = 1;
			time.sleep(20)
			continue

		else: 

			print now + ": Network down\nAttempting reconnect in 30 seconds.."

	# Check every 60 seconds
	time.sleep(30)



