#
# mustached-pi-client
#
# The rasperry pi client for mustached-pi-server
#
# (c)2013 The Mustached Pi Project
# http://github.com/mustached-pi
#
# Authors:
# - Angelo Lupo <angelolupo94@gmail.com>
# - Alfio E. Fresta <alfio.emanuele.f@gmail.com>
#

# Importing libraries 
import RPi.GPIO as GPIO # GPIO
import urllib2          # urllib2
import time             # Timing
import json             # JSON
import random           # Random functions
import sys

# Setting up GPIO to BCM notation
GPIO.setmode(GPIO.BCM)

# Do not be annoying if I change the mode of a channel
GPIO.setwarnings(False)

# Defining MUX's GPIO (Multiplexer Input/Output port)
MUXIO = 22

# Defining ALE's GPIO (ALE = Address Latch Enable)
ALE     = 0

# Server's mustached-pi-server installation directory (no final /)
BASEURL = "http://mustached-pi.alfioemanuele.it/fresta"

# Timing of the loop (how many seconds between sensors check)
WAIT    = 5

#Actives ALE (impulsive trigger)
def aleOn():
    GPIO.output(ALE, GPIO.HIGH)
    time.sleep(0.002)
    GPIO.output(ALE, GPIO.LOW)

# Read value from the port already set with setPort
def read():
    GPIO.setup(MUXIO, GPIO.IN)
    inval = GPIO.input(MUXIO)
    print "[INPUT] Value: %d" % inval
    return inval;

# Creates an pulse signal to MUX's out, to change flip flop state
def pulse():
    print "[PULSE] Pulse sent"
    GPIO.setup(MUXIO, GPIO.OUT)
    GPIO.output(MUXIO, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(MUXIO, GPIO.LOW)
    
# Function to generate a random MID
def generateMID():
    return str(random.randint(100000, 999999))

# Converts port's address from dec to bin and set the GPIO to the
# right logical level, then activates ALE
def setPort(port):
    print "[SET] Port %s" % port
    port = int(port)        # We need an integer for binary conversion
    portb = bin(port)       # Binary conversion...
    portb = portb.zfill(4)  # Makes a 4 digits binary number
                            # (Fills with zeros if needed)
                            
	# D -> MSB
    if portb[0] == "1":
    	GPIO.output(21,GPIO.HIGH)
    else:
    	GPIO.output(21,GPIO.LOW)
    # C
    if portb[1] == "1":
    	GPIO.output(17,GPIO.HIGH)
    else:
        GPIO.output(17,GPIO.LOW)
    # B
    if portb[2] == "1":
        GPIO.output(4,GPIO.HIGH)
    else:
        GPIO.output(4,GPIO.LOW)
    # A -> LSB
    if portb[3] == "1":
        GPIO.output(1,GPIO.HIGH)
    else:
        GPIO.output(1,GPIO.LOW)
    # Activating ALE...
    aleOn()


# Before doing anything, set ADDRESS PORTS as outputs
GPIO.setup(1,  GPIO.OUT) # A -> LSB
GPIO.setup(4,  GPIO.OUT) # B
GPIO.setup(17, GPIO.OUT) # C
GPIO.setup(21, GPIO.OUT) # D -> MSB
# Now remember setting the ADDRESS LATCH ENABLE as output
GPIO.setup(ALE, GPIO.OUT)



# Try reading the Machine code
try:
    fi   = open('MID', 'r')
    MID  = fi.read()
    fi.close()
   
except IOError:
    # If not, create a new one
    fi   = open('MID',  'w+')
    MID = generateMID()
    fi.write(MID)
    fi.close()


#Sets to 0 the array which contains the previous configuration
arrayprec = {}

# Sends MID and asks for a configuration array
while 1:
    
    try:
        f = urllib2.urlopen(BASEURL + '/endpoint.php', json.dumps({'sid':MID}))
        arrayconf = f.read()
        arrayconf = json.loads(arrayconf)
        
        if arrayconf["house"] is False:
            # The house is not configured
            print "[WARNING] House not configured"
            print MID # Shows the MID!
            print "I will check again in 10 seconds"
            time.sleep(10)
            
        else:
            # The house is configured
            print "[OK] House configuration found!"
            print arrayconf["house"]["name"]
            print arrayconf["house"]["address"]
            break; # Exit from the while!
            
    except:
        # If URL fetching has failed, maybe there is no connection...
        print "No internet connection"
        print sys.exc_info()[0]


#infinite loop
while 1:
#Loop -> changes the switch value if different from the previous configuration
#     -> saves values from sensors

	# Creates new dictionary to collect sensor data
	arrayread = {}
    
	# For each configured port from the server
	for (port, value) in arrayconf['ports'].iteritems():
        # Where:
        #  port     is the port number
        #  value -> {dictionary}
        #   value.type  is the port type ("input"/"output")
        #   value.value is the port value (0 or 1, only output case)
        
		# Setting up MUX port
		setPort(port)
        
		# Case output port
		if value["type"]=="output":
			if value["value"]!=arrayprec.get(port, 0):
				pulse()
				arrayprec[port]=value["value"]
                
		# Case input/sensor port
		if value["type"]=="input":
			arrayread[port]=read()
			temp = random.randint(0,255)
			arrayread[port]=temp

	# Converts the array into JSON
	arrayread = {'sid': MID, 'ports': arrayread}
	arrayread = json.dumps(arrayread)
    
	# Sends everything to the server
	f = urllib2.urlopen( BASEURL + '/endpoint.php',arrayread)
    
	# Reads the HTTP response for the next loop
	arrayconf = f.read()
	# print arrayconf # DEBUG
    
	# Decode JSON response into a dictionary
	arrayconf=json.loads(arrayconf)
    
	# Now wait before looping again
	time.sleep(WAIT)
