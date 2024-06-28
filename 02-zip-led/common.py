import machine
import utime


PRESS_DEBOUNCE_MS = 20

class Slot:
  def __init__(self, initial_value):
    self.value = initial_value

class FlagButton:
  def __init__(self, pin_number):
    self.pressed_ticks = None
    self.has_been_queried = False
    self.button = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_DOWN)

    def handler(pin):
      if pin.value():
        print(f"pressed, {self.pressed_ticks}, {self.has_been_queried}")
        if self.pressed_ticks is not None:
          return

        self.pressed_ticks = utime.ticks_ms()
        self.has_been_queried = False
      
        print(f"resulted in, {self.pressed_ticks}, {self.has_been_queried}")
  
      else:
        print(f"unpressed, {self.pressed_ticks}, {self.has_been_queried}")
        if self.pressed_ticks is None:
          return

        current_ticks = utime.ticks_ms()
        diff = utime.ticks_diff(current_ticks, self.pressed_ticks)
        if (diff >= PRESS_DEBOUNCE_MS):
          self.pressed_ticks = None

    self.button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handler)

  def get_once(self):
    if self.pressed_ticks == None or self.has_been_queried:
      return False
    self.has_been_queried = True
    return True

  def get(self):
    return self.pressed_ticks != None


def register_irq_falling(pin, time_slot, handler):
  def augmented_handler(passed_pin):
    current_ticks = utime.ticks_ms()
    diff = utime.ticks_diff(current_ticks, time_slot.value)
    if (diff >= PRESS_DEBOUNCE_MS):
      time_slot.value = current_ticks
      handler(passed_pin)

  pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=augmented_handler)
