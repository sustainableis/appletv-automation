#! /usr/bin/env python
import os;
import xml.etree.ElementTree as ET
import time
import applescript

userid_base = 1234

def create_user(name, test):
	shortname = name.replace(" " "")
	dscl = 'dscl . create /Users/'
	createUser = dscl + shortname
	setShell = dscl + shortname + ' UserShell /bin/bash'
	realName = dscl + shortname + ' RealName "' + name + '"'
	setID = dscl + shortname + ' UniqueID '  # append ID here 
	primaryGroup = dscl + shortname + ' PrimaryGroupID 1000'
	homeFolder = dscl + shortname + ' NFSHomeDirectory /Local/Users/' + shortname
	password = 'dscl . passwd /Users/' + shortname + ' PASSWD' # replace this
	homeFolderPath = '/Users/' + shortname

	if test:
		print createUser
		print setShell
		print realName
		print setID
		print primaryGroup
		print homeFolder

	else:
		os.system(createUser)
		os.system(setShell)
		os.system(realName)
		os.system(setID)
		os.system(primaryGroup)
		os.system(homeFolder)
		os.system('mkdir ' + homeFolderPath)
	
	return homeFolderPath


def create_config_file(url, appletv):

	with open("config.txt", 'w') as f:
		f.write(url + "\n")
		f.write(appletv + "\n")


def move_program_files(destPath):
	os.system('cp sis_dashboard_automation.py ' + destPath)
	os.system('cp automation_launcher.scpt ' + destPath)
	os.system('cp com.sis.automation_launcher.plist ' + destPath + '/Library/LaunchAgents/')
	os.system('mv config.txt ' + destPath)




# first check for root 
if os.geteuid() != 0:
	exit ("Installer must be run with root privileges!")

# now that we have root, easy-install py_applescript
print "Installing py-applescript.."
os.system("easy_install py-applescript")

# install ElementTree
print "Installing ElementTree"
os.system("easy_install elementtree")

# now we need to read the config file
config = ET.parse('display_config.xml')
root = config.getroot()

#get all the display 
displays = root.findall('display')

# create users and config files for each display
for display in root.findall('display'):

	# get url and appletv
	url = display.find('url').text.strip()
	appletv = display.find('appletv').text.strip()

	# username is the same as the appletv name
	path = create_user(appletv)

	# create script config file
	create_config_file(url, appletv)

	# move program files to newly created user folder
	move_program_files(path)


