#! /usr/bin/env python
import os
import xml.etree.ElementTree as ET
import time
import applescript

userid_base = 1234

def create_user(name, dryrun):
	global userid_base
	shortname = name.replace(" ", "")
	dscl = 'dscl . create /Users/'
	createUser = dscl + shortname
	setShell = dscl + shortname + ' UserShell /bin/bash'
	realName = dscl + shortname + ' RealName "' + name + '"'
	setID = dscl + shortname + ' UniqueID ' + str(userid_base)
	primaryGroup = dscl + shortname + ' PrimaryGroupID 1000'
	homeFolder = dscl + shortname + ' NFSHomeDirectory /Users/' + shortname
	password = 'dscl . passwd /Users/' + shortname + ' sis' # replace this


	print createUser
	print setShell
	print realName
	print setID
	print primaryGroup
	print homeFolder

	if not dryrun:
		os.system(createUser)
		os.system(setShell)
		os.system(realName)
		os.system(setID)
		os.system(primaryGroup)
		os.system(homeFolder)
		os.system(password)

		userid_base = userid_base + 1
	

def provision_user(name):

	shortname = name.replace(" ", "")
	destPath = '/Users/' + shortname

	#os.system('mkdir -p ' + destPath + '/Library/LaunchAgents/')
	os.system('cp sis_dashboard_automation.py ' + destPath)
	os.system('cp automation_launcher.scpt ' + destPath)
	#os.system('cp com.sis.automation_launcher.plist ' + destPath + '/Library/LaunchAgents/')
	os.system('mv config.txt ' + destPath)

def create_config_file(url, appletv):

	with open("config.txt", 'w') as f:
		f.write(url + "\n")
		f.write(appletv + "\n")


def enable_gui_scriptiong():
	os.system('./tccutil.py --insert com.apple.Terminal')
	os.system('./tccutil.py --enable com.apple.Terminal')

def install_applications():
	os.system('cp -R -n Google\\ Chrome.app /Applications/')
	os.system('cp -R -n AirParrot.app /Applications/')


# first check for root 
if os.geteuid() != 0:
	exit ("Installer must be run with root privileges!")

# now that we have root, easy-install py_applescript
print "Installing py-applescript.."
os.system("easy_install py-applescript")

time.sleep(2)

# install ElementTree
print "Installing ElementTree"
os.system("easy_install elementtree")

print "Enabling GUI scripting for Terminal.app"
enable_gui_scriptiong()

#print "Installing Chrome and AirParrot"
#install_applications()

# now we need to read the config file
config = ET.parse('display_config.xml')
root = config.getroot()


# create users and config files for each display
for display in root.findall('display'):

	# get url and appletv
	appletv = display.find('appletv').text.strip()
	url = display.find('url').text.strip()


	print 'Creating user "' + appletv + '"...'

	# username is the same as the appletv name
	create_user(appletv, False)

	#create_config_file(url, appletv)

	#provision_user(appletv)

	time.sleep(3)

print "Installation complete.  Log in each new user, set up Chrome, then run provision_users.py to complete setup."

