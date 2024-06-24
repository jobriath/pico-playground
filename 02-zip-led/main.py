import machine
import array
import time
from rp2 import PIO, StateMachine, asm_pio

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

button_r = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_g = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)

button_r_state = False
button_g_state = False
button_b_state = False

def button_r_handler(pin):
  global button_r_state
  print("r clicked")
  button_r_state = True
  
def button_g_handler(pin):
  global button_g_state
  button_g_state = True

def button_b_handler(pin):
  global button_b_state
  button_b_state = True

button_r.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_r_handler)
button_g.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_g_handler)
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_b_handler)

r = 0
g = 0
b = 0

while True:
  if button_r_state:
    if r >= 255:
      r = 0
    else:
      r += 32
    button_r_state = False
    print(f"clicked and handled and processed: {r}")
    time.sleep_ms(100)

  if button_g_state:
    if g >= 255:
      g = 0
    else:
      g += 32
    button_g_state = False
    time.sleep_ms(100)

  if button_b_state:
    if b >= 255:
      b = 0
    else:
      b += 32
    button_b_state = False
    time.sleep_ms(100)

  print(f"{r}:{g}:{b}")

  for i in range(num_leds):
    leds[i] = (g << 16) + (r << 8) + b

  zip_stick.put(leds, 8)

  time.sleep_ms(30)
  

  zip_stick.put(leds, 8)