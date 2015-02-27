#! /usr/bin/env python
import os
import xml.etree.ElementTree as ET


def provision_user(name):

	shortname = name.replace(" ", "")
	destPath = '/Users/' + shortname

	#os.system('mkdir -p ' + destPath + '/Library/LaunchAgents/')
	os.system('cp sis_dashboard_automation.py ' + destPath)
	#os.system('cp automation_launcher.scpt ' + destPath)
	#os.system('cp com.sis.automation_launcher.plist ' + destPath + '/Library/LaunchAgents/')
	os.system('mv config.txt ' + destPath)
	os.system('cp -R automation_launcher.app ' + destPath + "/Desktop/")
	os.system('cp airparrot_license.rtf ' + destPath + "/Desktop/")

def create_config_file(url, appletv):

	with open("config.txt", 'w') as f:
		f.write(url + "\n")
		f.write(appletv + "\n")

# first check for root 
if os.geteuid() != 0:
	exit ("Provisioning must be run with root privileges!")

# now we need to read the config file
config = ET.parse('display_config.xml')
root = config.getroot()

for display in root.findall('display'):

	appletv = display.find('appletv').text.strip()
	url = display.find('url').text.strip()

	print "Provisioning user /Users/" + appletv.replace(" ", "")

	# create config file for this user
	create_config_file(url, appletv)

	# provision this user's files
	provision_user(appletv)

print "Provisioning phase 2 complete.  To activate automation, set up applications on each account and start automation_launcher on the Desktop."
