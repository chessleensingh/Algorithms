Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> from pyfirmata import Arduino, ArduinoMega
from pyfirmata import util

from wyliodrin import *

from time import *

from threading import Timer

pulse = None
x = None
temp = None
y = None
z = None
count = None

def setBoard(boardType, port):
  if boardType == 'arduino':
    board = Arduino(port)
  else:
    board = ArduinoMega(port)
  return board
board=setBoard('arduino', '/dev/ttyACM0')
reader = util.Iterator(board)
reader.start()

pin_var = board.get_pin("d:4:o")

pin_var2 = board.get_pin("a:3:i")

pin_var3 = board.get_pin("a:0:i")

pin_var4 = board.get_pin("a:4:i")

pin_var5 = board.get_pin("a:1:i")

pin_var6 = board.get_pin("a:2:i")


count = 0
def loopCode():
  global pulse, x, temp, y, z, count
  pin_var.write(0)
  pulse = float (round((pin_var2.read() or 0) * 1023))
  x = float (round((pin_var3.read() or 0) * 1023))
  temp = float (round((pin_var4.read() or 0) * 1023))
  y = float (round((pin_var5.read() or 0) * 1023))
  z = float (round((pin_var6.read() or 0) * 1023))
  pulse = pulse + 200
  op_temp = temp / 13.13
  sendSignal('x', x)
  sendSignal('op_temp', op_temp)
  sendSignal('pulse', pulse)
  sendSignal('y', y)
  sendSignal('z', z)
  if count == 0:
    if op_temp > 36:
      pin_var.write(1)
      sleep ((3000)/1000.0)
      count = 1
  if op_temp < 36:
    count = 0
  Timer(0.02, loopCode).start()
loopCode()
