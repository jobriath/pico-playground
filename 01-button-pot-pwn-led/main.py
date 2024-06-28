import machine
import utime

button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
led = machine.PWM(machine.Pin(16))
led.freq(500)
pot = machine.ADC(26)

class Slot:
  def __init__(self, initial_value):
    self.value = initial_value

PRESS_DEBOUNCE_MS = 20

def register_irq_falling(pin, time_slot, handler):
  def augmented_handler(passed_pin):
    current_ticks = utime.ticks_ms()
    diff = utime.ticks_diff(current_ticks, time_slot.value)
    if (diff >= PRESS_DEBOUNCE_MS):
      time_slot.value = current_ticks
      handler(passed_pin)

  pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=augmented_handler)



isButtonDown = False
button_pressed_time = Slot(0)
def button_pressed(pin):
  global isButtonDown
  isButtonDown = not isButtonDown
register_irq_falling(button, button_pressed_time, button_pressed)



while True:
  # TODO: Needs calibrating!
  # Project idea: Sleepy mode.
  pot_value = pot.read_u16()
  if isButtonDown:
    led.duty_u16(pot_value)
  else:
    led.duty_u16(0)

