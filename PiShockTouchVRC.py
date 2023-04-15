import requests
from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import math
from configparser import ConfigParser
import time


Pi_intensity = 15
Pi_duration = 1
Pi_mode = 2
Pi_username = ""
Pi_sharecode = ""
Pi_apikey = ""

Pi_delay = 0 # delay between requests
Pi_last_shock = 0

Pi_DEBUG = False
Pi_SIMULATE = False # if true just log the command and dont send it

def BuildCommandJSON():
  
    Command = {
        "username":Pi_username,
        "Name":"PiShockTouchVRC",
        "Code":Pi_sharecode,
        "Intensity":Pi_intensity,
        "Duration":Pi_duration,
        "Apikey":Pi_apikey,
        "OP":Pi_mode,
    }

    if Pi_DEBUG:
        print("Printing API Request for Debug")
        print(Command)
  
    return Command

def TestBeep():
  
    Command = {
        "username":Pi_username,
        "Name":"PiShockTouchVRC",
        "Code":Pi_sharecode,
        "Intensity":Pi_intensity,
        "Duration":Pi_duration,
        "Apikey":Pi_apikey,
        "OP":2,
    }
    if Pi_DEBUG:
        print("Printing API Request for Debug")
        print(Command)
    return Command



def ParseConfig():
    global Pi_username
    global Pi_sharecode
    global Pi_apikey

    global Pi_intensity
    global Pi_duration
    global Pi_mode
    
    global Pi_delay
    
    global Pi_DEBUG
    global Pi_SIMULATE
    
    config=ConfigParser()
    config.read('pishock.cfg')

    # read API config 
    Pi_username=config['API']['USERNAME']
    Pi_apikey=config['API']['APIKEY']
    Pi_sharecode=config['API']['SHARECODE']

    # read SETTINGS
    Pi_intensity=config['SETTINGS'].get('INTENSITY', 15)
    Pi_duration=config['SETTINGS'].get('DURATION', 1)
    Pi_mode=config['SETTINGS'].get('MODE', "beep")
    Pi_delay= int(config['SETTINGS'].get('DELAY', '0'))

    Pi_DEBUG=config['SETTINGS'].get('DEBUG', False)
    Pi_SIMULATE=config['SETTINGS'].get('DEBUG', False)

    # translate mode to number
    if(Pi_mode == "vibe"): 
        Pi_mode = 1
    elif(Pi_mode == "beep"): 
        Pi_mode = 2
    elif(Pi_mode == "zap"): 
        Pi_mode = 0
    else:
        Pi_mode = 2



    print("User configuration found!")
    print("Username:",Pi_username)
    print("Sharecode:",Pi_sharecode)
    print("API Key: ",Pi_apikey)
    print("*"*40)
    print("Sending test beep...")
    if(SendTest() == 200):
        print("API Request success! Happy zapping!")
    else:
        print("Test failed! Please check collar connection and power.")


def SendTest():
    if Pi_SIMULATE:
        print('!! SIMULATED REQUEST !!')
        TestBeep()
        return 200
    r = requests.post('https://do.pishock.com/api/apioperate/',json=TestBeep())
    print(r.status_code)
    return r.status_code

def SendRequest():
    global Pi_last_shock
    global Pi_delay

    current_time = time.monotonic()
    # check delay
    if (Pi_last_shock + Pi_delay > current_time):
        print ('please wait', math.trunc(Pi_last_shock + Pi_delay - current_time) , 'secounds')
        return 429 # return 429 "Too many requests"
    
    Pi_last_shock = current_time

    if Pi_SIMULATE:
        print('!! SIMULATED REQUEST !!')
        TestBeep()
        return 200
    r = requests.post('https://do.pishock.com/api/apioperate/',json=BuildCommandJSON())
    print(r.status_code)
    return r.status_code


def detection_handler(address, *args):
    global Pi_intensity
    global Pi_mode
    global Pi_duration
    #print(f"{address}: {args}") #Default print all for debug
        
    if(address == "/avatar/parameters/PiShock_CollarTouch"):
      if(args[0] > 0): 
        print(f"Detection Touch {address}: {args}")
        SendRequest()
    elif(address == "/avatar/parameters/PiShock_Intensity"):
        if(args[0] > 0): 
            Pi_intensity = math.trunc(args[0] *100)
            print("Normalized intensity: ",Pi_intensity)
    elif(address == "/avatar/parameters/PiShock_Duration"):
        if(args[0] > 0): 
            Pi_duration = math.trunc(args[0]*15)
            if(Pi_duration < 1):
                Pi_duration = 1
            print("Normalized duration: ",Pi_duration)
    elif(address == "/avatar/parameters/PiShock_Mode"):
        if(args[0] == 1): 
            Pi_mode = 1
            print("Vibe")
        elif(args[0] == 2 or args[0] == 0): 
            Pi_mode = 2
            print("Beep")
        elif(args[0] == 3): 
            Pi_mode = 0
            print("Zap")
    elif(address == "/avatar/parameters/PiShock_Test"):
        if(args[0] > 0): 
            print(f"Detection Touch {address}: {args}")
            SendRequest()


     
def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}") #Default route when not detecting


ParseConfig()
dispatcher = Dispatcher()
dispatcher.map("/avatar/*", detection_handler)
dispatcher.set_default_handler(default_handler)

ip = "127.0.0.1"
port = 9001





server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()
    
    

