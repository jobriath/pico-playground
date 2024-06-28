import machine
import utime


PRESS_DEBOUNCE_MS = 20

class Slot:
  def __init__(self, initial_value):
    self.value = initial_value

class FlagButton:
  def __init__(self, pin_number):
    self.pressed = False
    self.last_ticks = utime.ticks_ms()
    self.button = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_DOWN)

    def handler(pin):
      current_ticks = utime.ticks_ms()
      diff = utime.ticks_diff(current_ticks, self.last_ticks)
      if (diff >= PRESS_DEBOUNCE_MS):
        self.last_ticks = current_ticks
        self.pressed = True

    # TODO: A long press might erroneously fire on release.
    self.button.irq(trigger=machine.Pin.IRQ_FALLING, handler=handler)

  def get_and_clear(self):
    result = self.pressed
    self.pressed = False
    return result


def register_irq_falling(pin, time_slot, handler):
  def augmented_handler(passed_pin):
    current_ticks = utime.ticks_ms()
    diff = utime.ticks_diff(current_ticks, time_slot.value)
    if (diff >= PRESS_DEBOUNCE_MS):
      time_slot.value = current_ticks
      handler(passed_pin)

  pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=augmented_handler)
