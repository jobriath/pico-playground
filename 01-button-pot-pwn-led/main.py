import machine
import utime

button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
led = machine.PWM(machine.Pin(16))
led.freq(500)
pot = machine.ADC(26)

isButtonDown = False

# TODO: Needs debouncing!
def button_irq_handler(pin):
  global isButtonDown
  print("click", pin)
  isButtonDown = not isButtonDown

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_irq_handler)

while True:
  # TODO: Needs calibrating!
  # Project idea: Sleepy mode.
  pot_value = pot.read_u16()
  if isButtonDown:
    led.duty_u16(pot_value)
  else:
    led.duty_u16(0)

