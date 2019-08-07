# py_thorlabs_ctrl
Python package for controlling Thorlabs hardware. This is a wrapper for Kinesis .NET APIs. I got the idea from Stuart's repository [thorlabs_kenesis_python](https://github.com/trautsned/thorlabs_kenesis_python), packaged the APIs and wrote the tests. .NET APIs are easy to understand and implement, and I prefer this method over some other techniques like C binding.

Currently this package only supports some T-Cube and K-Cube motion controllers, but the code can be easily extended to support other hardware like laser diodes. Hope this can help anyone who hopes to use Python to control Thorlabs hardware but has little clue where to start.

There is also an APT module that uses the legacy ActiveX controls, which can be used with Qt, but has not been tested yet.

Other related packages:
* [nelsond/thorlabs-mtd415t](https://github.com/nelsond/thorlabs-mtd415t)
* [qpit/thorlabs_apt](https://github.com/qpit/thorlabs_apt)
* [ekarademir/thorlabs-kinesis](https://github.com/ekarademir/thorlabs-kinesis)

**not an official package**

## Example

```Python
>>> import py_thorlabs_ctrl.kinesis
>>> py_thorlabs_ctrl.kinesis.init(r'C:\Program Files\Thorlabs\Kinesis') 
       # change this to your own installation path
>>> from py_thorlabs_ctrl.kinesis.motor import KCubeDCServo
>>> tcube = TCubeDCServo(83854669)
>>> tcube.create()
>>> tcube.enable()
>>> tcube.is_homed()
False
>>> tcube.get_position()
18.32
>>> tcube.home() # wait a while
>>> tcube.move_absolute(34) # wait
>>> tcube.get_position()
34
>>> tcube.disable()
>>> tcube.disconnect()
```

## Prerequisites

* [Thorlabs Kinesis® Software](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285)
* [Python for .NET](https://github.com/pythonnet/pythonnet)

## API reference

### Initialize

```Python
import py_thorlabs_ctrl.kinesis
py_thorlabs_ctrl.kinesis.init(kinesis_installation_path)
```

MUST do this first. The init function automatically determines if the installation path is valid (must contain `Thorlabs.MotionControl.Controls.dll`).

### create an instance of a motor

```Python
from py_thorlabs_ctrl.kinesis.motor import KCubeDCServo
motor = KCubeDCServo(serial_number)
```

Currently supports `KCubeDCServo`, `TCubeDCServo` and `TCubeStepper`.

### check if motor is in home position

`motor.is_homed()`

### move the motor to home position

`motor.home()`

### move with a relative distance (this function and the following one both return immediately. May provide a locked version later)

`motor.move_relative(distance)`

### move to an absolute position

`motor.move_absolute(position)`

### check current position

`motor.get_position()`

### set velocity and acceleration

`motor.set_velocity(max_velocity = None, acceleration = None)`

### disconnect a motor 

```Python
motor.disable()
motor.disconnect()
```

### specific to K-Cubes:

set joystick mode to "velocity control" (the motor always sets itself to jog mode after connection):

`motor.set_joystickmode_velocity()`

set display intensity (again, it always resets after connection)

`motor.set_display_intensity(intensity)`

set display timeout

`motor.set_display_timeout(timeout)`
