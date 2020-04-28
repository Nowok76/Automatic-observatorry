#####################################################################
#                                                                   #
#                   Copyright(c) 2020                               #
#       Dariusz Nowakowski  <bozondn AT gmail DOT com>              #
#                   www.astrobudka.pl                               #
#####################################################################

import RPi.GPIO as GPIO
import os
import time


def roof():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(04, GPIO.OUT)              # set GPIO pin on your Rpi
        GPIO.output(04, GPIO.LOW)
        time.sleep(3)
        GPIO.output(04, GPIO.HIGH)
        GPIO.cleanup()
	print "I'm  closing roll off roof"
	time.sleep(8)                             # set closing roll off roof time
	print "The Roll off roof has been closed"

while True:
	dePos = os.popen('indi_getprop -1 -h Rpi_IP -p 7624 "EQMod Mount.CURRENTSTEPPERS.DEStepsCurrent"')        # checks DE encoder positions 
	pos1 = dePos.read()
	s = pos1
	parkDE = s.strip()
	DE = "7509738"   # set your DE encoders parking positions

	raPos = os.popen('indi_getprop -1 -h Rpi_IP -p 7624 "EQMod Mount.CURRENTSTEPPERS.RAStepsCurrent"')        # checks RA encoder positions 
	pos2 = raPos.read()
	s = pos2
	parkRA = s.strip()
	RA = "10454592"  # set your RA encoders parking positions

	if DE == parkDE and RA == parkRA:
		roof()
#-------disconnect devaces
		print "Turning off devices"
		time.sleep(2)
		os.popen ("ssh astroberry@192.168.55.202 qdbus org.kde.kstars /KStars/Ekos org.kde.kstars.Ekos.disconnectDevices")   # astroberry@YOUR_ IP
		print "Devicess disconected"
		time.sleep(2)
		os.popen ("ssh astroberry@192.168.55.202 qdbus org.kde.kstars /KStars/Ekos org.kde.kstars.Ekos.stop")
		print "INDI disconected"
		time.sleep(2)
		os.popen ("ssh astroberry@192.168.55.202 killall kstars")
		print "Kstars off"
		time.sleep(2)
		os.popen ("echo astroberry | ssh -tt astroberry@192.168.55.202 sudo poweroff")
		print "Astroberry Server shutting down"
		time.sleep(10)
#-------setup off----------
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)
		GPIO.output(18, GPIO.HIGH)
		GPIO.setwarnings(False)
		print "Power is off"

		break
	else:
		print "Mount is not parked yet"
	time.sleep(300)      # set up time of checking parkposition interval
