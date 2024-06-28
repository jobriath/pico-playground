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

def components(bits):
  r = (bits >> 8) & 0xff
  g = (bits >> 16) & 0xff
  b = bits & 0xff
  return (r, g, b)

DELTA_MS = 30
RETAIN = 0.9  # 0.5 * (1 / DELTA_MS)  # Half-life of a second
LOSE = 1 - RETAIN

while True:
  r = 255 if button_r.get() else 0
  g = 255 if button_g.get() else 0
  b = 255 if button_b.get() else 0

  for i in reversed(range(num_leds)):
    (lr, lg, lb) = components(leds[i - 1]) if i > 0 else (r, g, b)
    (fr, fg, fb) = components(leds[i])
    nr = int(RETAIN * fr + LOSE * lr)
    ng = int(RETAIN * fg + LOSE * lg)
    nb = int(RETAIN * fb + LOSE * lb)
    leds[i] = (ng << 16) + (nr << 8) + nb

  zip_stick.put(leds, 8)

  time.sleep_ms(DELTA_MS)
