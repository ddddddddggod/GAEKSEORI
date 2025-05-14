import RPi.GPIO as GPIO  
import Adafruit_DHT  
import time

sensor = Adafruit_DHT.DHT11  # for DHT11
ht_pin = 21  # DHT11 pin number
servo_pin = 12   # servo pin number
humidity,temperature= Adafruit_DHT.read_retry(sensor,ht_pin)

# GPIO Initialization
GPIO.setmode(GPIO.BCM)        
GPIO.setup(servo_pin, GPIO.OUT)  

servo = GPIO.PWM(servo_pin, 50)  # Using the servo pin in PWM mode at 50 Hz (50Hz > 20ms)
servo.start(0)  # Servo PWM start duty = 0, when duty is 0, servo does not work


def set_angle(angle):
    duty = angle / 18 + 2  # duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    servo.ChangeDutyCycle(0)

if humidity is not None and temperature is not None:
    if humidity >= 65:  
        print('temperature={0:0.1f}*C  humidity={1:0.1f}%, Water tank open!'.format(temperature, humidity))
        set_angle(90)    #water tank close (first location)
        time.sleep(1) 

    # water tank open
        set_angle(180)
        time.sleep(30)  

        servo.stop()
        GPIO.cleanup()

    else:
        print('temperature={0:0.1f}*C  humidity={1:0.1f}%'.format(temperature, humidity))
        set_angle(90)   #water tank close
        time.sleep(100)  
else:
    print('Failed to get reading. Try again!')

    servo.stop()
    GPIO.cleanup()
