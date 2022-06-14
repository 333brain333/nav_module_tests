#!/usr/bin/env python3
import Jetson.GPIO as GPIO
from time import sleep
import time
import nav_modules_ips_to_ping 
import logging
import subprocess
from datetime import datetime
from threading import Thread

def StateMachine(devs:list)->dict:
    '''
    Returns a dict with a given ips as
    a keys and 0 as a respective value
    '''
    return dict(zip(devs, [0]*len(devs)))

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
            logging.info(f'Initialized {gpio_out} GPIO as OUTPUT')
        if gpio_in:
            GPIO.setup(gpio_in, GPIO.IN)
            logging.info(f'Initialized {gpio_in} GPIO as INPUT')
    def clean(self):
        '''
        Cleanup all states. Use at program close. 
        '''
        GPIO.cleanup()
        logging.info('Cleaned all GPIOs')
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


class PingDeviceClass():
    '''
    Starts a thread for a given list of a ip addresses.
    Each thread pings given ip and adds relust into a queue
    '''
    def __init__(self, ip_list:list, states:dict)->None:
        self.ip_list = ip_list
        self.states = states
    def thread_pinger(self,
                      i:int,
                      ip_addr,
                      )->None:
        '''
        Pings given IP in a thread and puts 0/1 result in
        a queue. Adds an error into the error queue if defined.
        '''
        global reboot_time
        while True:
            p_ping = subprocess.Popen(["ping", "-c", "4", "-W", "1", "-I","eth0", ip_addr],
                                       shell = False, stdout = subprocess.PIPE)
            if p_ping.wait() == 1 and\
                    (time.time()-reboot_time)>60\
                    and self.states[ip_addr] == 0:
                self.states[ip_addr] = 1
                logging.info(f'{pretty_time()}: {ip_addr} becomes NOT ACCESSIBLE')
            elif p_ping.wait() == 0 and\
                    self.states[ip_addr] == 1:
                self.states[ip_addr] = 0
                logging.info(f'{pretty_time()}: {ip_addr} becomes ACCESSIBLE')
    def run(self)->None:
        '''
        Starts threads that will ping each ip in the
        given ip list
        '''
        for i in range(len(self.ip_list)):
            thread = Thread(target=self.thread_pinger,
                            args=[i,
                                  self.ip_list[i],
                                  ],
                            name=f'PingDevice{self.ip_list[i]}',
                            daemon=True)
            thread.start()

def pretty_time()->str:
    '''
    Returns string with a datetime
    '''
    return datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

def main()->None:
    '''
    Main function
    '''
    logging.basicConfig(filename=f'debug_log_{pretty_time()}.txt', level=logging.DEBUG)
    ip_list = nav_modules_ips_to_ping.list
    states = StateMachine(ip_list) 
    relay = J_21(gpio_out = [12])
    ping = PingDeviceClass(ip_list, states) 
    ping.run()
    cur_time = time.time()
    global reboot_time
    reboot_time = cur_time
    logging.info(f'Test started at {pretty_time()}')
    try:
        while True:
            if time.time()-cur_time > 3600:
                print("TRUE")
                relay.write(12, False)
                sleep(3)
                relay.write(12, True)
                logging.info(f'Rebooted nav modules at {pretty_time()}')
                reboot_time = time.time()
                cur_time = time.time()
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        relay.clean()
        logging.info('Test finished')

if __name__=="__main__":
    main()

