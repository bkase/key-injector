from Quartz import *
from socket import *
import keycode
import os

SOCKET = '/tmp/keys.sock'

def keycodify(key):
  if type(key) != int:
    return keycode.tokeycode(key)
  else:
    return key

def makeTap(key):
  return makeDown(key) + makeUp(key)

def makeDown(key):
  return [ CGEventCreateKeyboardEvent(None, keycodify(key), True) ]

def makeUp(key):
  return [ CGEventCreateKeyboardEvent(None, keycodify(key), False) ]

def post(events):
  [ CGEventPost(kCGSessionEventTap, e) for e in events ]

lastDownKey = None
try:
  server = socket(AF_UNIX, SOCK_DGRAM)
  server.bind(SOCKET)
  while True:
    data = server.recv(16).strip()
    print "Got:", data
    cmd = None
    if len(data) is 1:
      cmd = ' '
    elif len(data) is 2:
      cmd = data[1]
    else:
      if data[1:] == "Left":
        cmd = 0x7B
      elif data[1:] == "Right":
        cmd = 0x7C
      elif data[1:] == "Down":
        cmd = 0x7D
      elif data[1:] == "Up":
        cmd = 0x7E
      else:
        raise "bad cmd"

    if data[0] is 'u':
      post(makeUp(cmd))
      lastDownKey = None
    elif data[0] is 'd':
      post(makeDown(cmd))
      lastDownKey = cmd
    else: # data[0] is 't':
      post(makeTap(cmd))
finally:
  if lastDownKey is not None:
    post(makeUp(lastDownKey))
  os.unlink(SOCKET)

