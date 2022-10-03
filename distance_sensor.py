
#from machine import Pin, I2C
#from ssd1306 import SSD1306_I2C
from neopixel import Neopixel
from machine import Pin
import utime
import time

#Initialize some debug variables
#debug = True
debug = False
distanceStr = '{distanceFloat:.1f} cm'

trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)

numpix = 30
strip = Neopixel(numpix, 0, 28, "RGB")

# Distance in CM
minDistance = 5.0
maxDistance = 60.0
mainLedDistance = 0

# Initialize system time
mainTime = time.time()
#Timeout to turn LEDs off ( in seconds)
ledTimeout = 20

# #Color LUTs
# red = (255, 0, 0)
# orange = (255, 50, 0)
# yellow = (255, 100, 0)
# green = (0, 255, 0)
# blue = (0, 0, 255)
# indigo = (100, 0, 90)
# violet = (200, 0, 100)
blank = (0, 0, 0)
# colors_rgb = [red, orange, yellow, green, blue, indigo, violet]


def get_ultrasonic_distance():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
       
   timepassed = signalon - signaloff
   #print(timepassed)
   distance = (timepassed * 0.0343) / 2
   #distance = "{:.1f}".format(distance)
   
   #print(distance + " cm")
   
   return distance


while True:
    strip.brightness(100)
    
    distance = get_ultrasonic_distance()

    #Beyond 100cm the results are not terribly accurate so clamp values
    if distance > maxDistance:
        distance = maxDistance
        
    #Assign LED color    
    led_color = (255, 0, 0) #green

    if (distance <= ((maxDistance + minDistance) * 0.5)):
        led_color = (120, 254, 0) #yellow
    if (distance <= (minDistance * 2)):
        led_color = (0, 255, 0) #red
    
    #Determine what LEDs need to be illuminated by normalizing the
    #distance parameter against min/max
    normalizedDistance = (distance - minDistance) / (maxDistance - minDistance)
    ledDistance = round(normalizedDistance * numpix)   
    
    currentTime = time.time()
    timeDelta = currentTime - mainTime
    
    if (ledDistance == mainLedDistance) and (timeDelta < ledTimeout):
        if debug:
            print('Run LEDs')
            print('Time: '+ str(timeDelta))
            print(distanceStr.format(distanceFloat = distance))
            
        #Start strip
        #Begin blinking if distance is within minDistance
        if distance < minDistance:
            for x in range(numpix):
                strip.set_pixel(x, led_color)
            strip.show()
            utime.sleep(0.1)
            for x in range(numpix):
                strip.set_pixel(x, blank)
            strip.show()
            utime.sleep(0.1)
            
        #If the distance isn't within minDistance then run the standard
        #LED routine
        else:    
            mainLedDistance = ledDistance
            
            for x in range(ledDistance):
                strip.set_pixel(x, led_color)
            strip.show()             
                   
    else:
        #Timed out
        #Reinitialize timers
        if (ledDistance == mainLedDistance):
            #If we have reached our timeout limit and distance isnt changing much
            #disable the LEDs
            if debug:
                print('Nothing to do here...')
            strip.fill(blank)
            strip.show()
            
        else:
            #This condition is triggered if the timeout is reached but the distance
            #begins to change.  Reinitialize distance and time tracking vars
            mainLedDistance = ledDistance
            mainTime = currentTime
            
            if debug:
                print('**** Resetting timeout ***')

    #utime.sleep(0.2)
    strip.fill(blank)