'''
Helps check whether the relay connected to the GPIO header is working or not
Press any button to switch relay state. Press CTRL+C to exit
'''
import J_21
import sys

if __name__=="__main__":
    relay = J_21.J_21(gpio_out=[12])
    print("Press Enter to switch relay state")
    init_state = False
    try:
        while True:
            input('Press Enter')
            relay.write(12, init_state)
            init_state = not init_state
    except KeyboardInterrupt:
        relay.clean()
        sys.exit(0)
