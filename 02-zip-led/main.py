import machine
import array
import time
from rp2 import PIO, StateMachine, asm_pio

from common import FlagButton

num_leds = 5

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def output_zip_led():
  wrap_target()
  label("bitloop")
  out(x, 1)             .side(0) [2]
  jmp(not_x, "do_zero") .side(1) [1]
  jmp("bitloop")        .side(1) [4]
  label("do_zero")
  nop()                 .side(0) [4]
  wrap()

zip_stick = StateMachine(0, output_zip_led, freq=8000000, sideset_base=machine.Pin(19))
zip_stick.active(1)

leds = array.array("I", [0 for _ in range(num_leds)])

button_r = FlagButton(10)
button_g = FlagButton(11)
button_b = FlagButton(12)

r = 0
g = 0
b = 0

while True:
  if button_r.get_and_clear():
    if r >= 255:
      r = 0
    else:
      r += 32
    time.sleep_ms(100)

  if button_g.get_and_clear():
    if g >= 255:
      g = 0
    else:
      g += 32
    time.sleep_ms(100)

  if button_b.get_and_clear():
    if b >= 255:
      b = 0
    else:
      b += 32
    time.sleep_ms(100)

  print(f"{r}:{g}:{b}")

  for i in range(num_leds):
    leds[i] = (g << 16) + (r << 8) + b

  zip_stick.put(leds, 8)

  time.sleep_ms(30)
