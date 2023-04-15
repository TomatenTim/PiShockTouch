# PiShockTouch
PiShockTouch is an open source application that allows the PiShockCollar to become interractive to touch in VR Chat.

## Disclaimer
I am not affiliated, associated, authorized, endorsed by, or in any way officially connected with PiShock

This code was forked from [DesMakesStuff/PiShockTouch](https://github.com/DesMakesStuff/PiShockTouch) to customize it.

Following things are modified:
  - changed Avatar Parameters
  - changed the way to set modes
  - code refactoring
  - added delay between requests



# How it Works
PiShockTouch relies on a VRC contact receiver to determine if someone has poked your collar. You can configure the poke to do anything the collar can do, adjusting for duration and intensity from the menu.



# How to use PiShockTouch

# Setting up your avatar requirements


1. Add a component to the PiShockCollar Asset or collar found in the PiShock discord. The component is called "VRC Contact Receiver"

2. Under the VRC Contact Receiver window configure the options of the shape and the radius you want the receiver to activate on. Check allow others(Safety settings will let you change in game who can interact with this receiver)

4. Add a collision tag for any bone to activate this collider I suggest doing the finger bone as it will cut down on false triggers.

5. Set the receiver type to constant

6. Type the parameter name as CollarTouch


![image](https://user-images.githubusercontent.com/102766533/197355966-342288aa-b97d-44be-acee-ced53219ea90.png)




8. Navigate to your network synced parameters. You can find this under you avatar descriptor usually labelled "Parameters". Add the following parameters:

![image](https://user-images.githubusercontent.com/102766533/197355844-be871070-788c-4e2a-a2ca-9399c5b8851b.png)


`PiShock_CollarTouch` bool

`PiShock_Intensity` float

`PiShock_Duration` float

`PiShock_Mode` int

`PiShock_Test` bool (optional)

![image](https://raw.githubusercontent.com/TomatenTim/PiShockTouch/56e9ef537f063814653656bd3764adc604e72b61/images/Parameters.png)


9. Add a Submenu with Buttons / Toggles to your Avatar
![image](https://raw.githubusercontent.com/TomatenTim/PiShockTouch/56e9ef537f063814653656bd3764adc604e72b61/images/Submenu.png)



# Setting up The application
1. Copy the `pishock.example.cfg` to `pishock.cfg`
4. Open the `pishock.cfg` and add your PiShock Username behind `USERNAME=`
3. Navigate to your PiShock account page and generate a new api key and add it behind `APIKEY=` in the config
4. Generate a new sharecode specifically for PiShockTouch, add limits for safety if needed and add it behind `SHARECODE=` in the config
5.  You can change the default `INTENSITY` (0 - 100), `DURATION` (in seconds) and `MODE` (`vibe`, `beep` or `zap`) in the config too. (these are applied when you start the script and can be changed within VRChat using your avatar menu)
6. You can also set the minimum delay in the config after `DELAY=`. The delay is the minimum time in seconds after a shock it waits before sending a new one.


# Install requirements

1. Install python
1. Use `pip install -r requirements.txt` to install all requirements

# Start the application

1. Ensure your collar is connected, online, and powered. 

2. If all information is correct you can open `start.bat`. The test should return 200 successful and your collar will beep once.  

3. You are ready to go! Hop in game and access the PiShock menu to change things such as intensity duration and swap modes.

# In game settings

All PiShock settings can be managed through the ingame menu


Intensity is 1 to 1 with the normal PiShock settings from 1% to 100%

Duration is a percentage of the max time(15 seconds). Example 50% is around 7 seconds

The mode can be set using 3 different Toggles

`Vibrate`

`Beep`

`Shock`

**TODO: add image**


