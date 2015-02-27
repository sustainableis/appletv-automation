----Starting state----
A mac mini running the latest version of Yosemite, connected to a 1080p monitor.  Chrome and AirParrot 1.x installed in /Appplications.  (I had the idea to distribute the apps with the automation software, that way everything you'd need would be on a usb stick or something.)

----The config file----
The config file for provisioning is a simple XML file:

<?xml version="1.0" encoding="UTF-8"?>
<sis_display_config>

	<display>
		<url>		
			http://lineage.sustainableis.com/facility/yRb7kzU0i5c3mxI7hR5w/blast
		</url>
		<appletv>
			Big Room
		</appletv>
	</display>

	<display>
		<url>		
			http://lineage.sustainableis.com/facility/yRb7kzU0i5c3mxI7hR5w/blast
		</url>
		<appletv>
			Apple TV
		</appletv>
	</display>

	<display>
		<url>		
			http://lineage.sustainableis.com/facility/yRb7kzU0i5c3mxI7hR5w/blast
		</url>
		<appletv>
			Dashboard
		</appletv>
	</display>

</sis_display_config>

This is where you pair up the desired AppleTV name and URL to display in chrome.  Add additional <display> tags as needed.

----Provisioning---
Provisioning is done in xx steps:

Step 1: Open terminal, cd to where the automation files are, and run provision_phase_1.py with sudo
   - If you're not root it'll complain and do nothing.  
   - Phase 1 of provisioning installs the necessary python libraries, enables GUI scripting (for security reasons, Mac OS only allows authorized applications to automate the GUI), and creates user accounts. 
   - After this step, a new user account will be created for each AppleTV in the config file.  The passwords for these new accounts are all "sis."

Step 2: Manually log in to each user account.  
   - This is necessary because I could not find a way to script the process that the Mac goes through on first login to a new account.  
   - You'll have to skip all the iCloud crap, and get to the desktop.  
   - Much faster if you enable fast user switching in "Login Options" under "User & Groups" in System preferences.  I could probably script this but it would be hard since it requires authentication. 
   - Once you've done this for all accounts, go back to the account you originally used to run provision_phase_1.py.

Step 3: Run provision_phase_2.py with sudo. This does the following:
   - Copies the automation executables to the appropriate places in the user accounts
   - Creates a config file for each user account's automation script to read, telling it which AppleTV to target and which URL to display, and copies it to the appropriate place
   - Copies the AirParrot license file to each new user's desktop

Step 4: Switch to each user account, and go through initial starts of Chrome and AirParrot:
   - For Chrome, you have to set it as the default browser
   - For AirParrot, you have to activate it (provision_phase_2.py placed the AirParrot license file on the desktop) and then close it, open it again and finally tell it not to auto update.

---Running the automation---
You can now double-click "automation_launcher" on each account's desktop.  This will start the automation script, opening chrome with the proper URL and connecting to the target AppleTV. It is best to verify that the dashboard is displaying prior to switching to the next account.  Now the system will detect and reconnect network outages on its own.  In addition, the automation script will disable sleeping/screensaver/stand-by on the mac mini.  