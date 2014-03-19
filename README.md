# Key Injector for OSX

Listen for keyboard commands and inject keyboard events to the OS. This is useful for hacking together hotkeys with non-standard keyboards (like a leap motion or foot pedal) or making a simple joystick "driver" (if you could call it that).

## How it works

Listen on a unix domain socket at `/tmp/keys.sock` for commands with a simple protocol (as described below) and convert these to keyboard events:

In OSX's Quartz library, there are functions `CGEventCreateKeyboardEvent` and `CGEventPost` which create and post keyboard events as if they had come from a keyboard.

You could probably easily get this working with Windows or Linux by replacing Quartz calls with proper keyboard event creation/posting calls.

## Install

```bash
git clone git@github.com:bkase/key-injector.git
git clone git@github.com:abarnert/pykeycode.git
cd pykeycode
python setup.py install
```

## Run

```bash
python key_injector.py
```

## Command protocol

Send one of the following onto the unixgram socket:

* u + key (release key key)
* d + key (press key key)
* t + key (tap key key)

Where key is either:

* [a-z] or [0-9] or other non-whitespace characters
* a space
* Left, Up, Right, or Down (corresponding to arrow keys)

examples:

* dLeft
* dt
* uLeft
* ut
* tg

## TODO (if you want to contribute):

* Make protocol less hacky
* Support other keys
