import Jetson.GPIO as GPIO
'''
Class that allowes to write/read j21 header's GPIO
'''
class J_21():
    '''
    Initializes GPIO of the Jetson TX2
    Has several meethods for GPIO control
    '''
    def __init__(self, gpio_out:list=None,gpio_out_init:bool=False, gpio_in:list=None):
        GPIO.setmode(GPIO.BCM)
        if gpio_out:
            if gpio_out_init:
                GPIO.setup(gpio_out, GPIO.OUT, initial=GPIO.HIGH)
            else:
                GPIO.setup(gpio_out, GPIO.OUT, initial=GPIO.LOW)
            print(f'Initialized {gpio_out} GPIO as OUTPUT')
        if gpio_in:
            GPIO.setup(gpio_in, GPIO.IN)
            print(f'Initialized {gpio_in} GPIO as INPUT')
    def clean(self):
        '''
        Cleanup all states. Use at program close. 
        '''
        GPIO.cleanup()
        print('Cleaned all GPIOs')
    def write(self, gpio:int, state:bool):
        '''
        Write output pin to desired value (HIGH\LOW)
        '''
        if state:
            GPIO.output(gpio, GPIO.HIGH)
        else:
            GPIO.output(gpio, GPIO.LOW)

    def read(self, gpio:int):
        '''
        Returns input pin value
        '''
        return GPIO.input(gpio)

