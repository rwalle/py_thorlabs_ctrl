import py_thorlabs_ctrl.kinesis
import clr, time

POLLING_INTERVAL = 250
ENABLE_SLEEP_TIME = 0.1

py_thorlabs_ctrl.kinesis.check_import()
  
from System import String
from System import Decimal
from System import Enum

clr.AddReference('System.Collections')
   
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")

import Thorlabs.MotionControl.DeviceManagerCLI
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
import Thorlabs.MotionControl.GenericMotorCLI

class MotorDirection(Enum):
    Forward=1
    Backward=2

class Motor:

    """
    Base class for Thorlabs motion controllers. Contains basic functions that apply to most controllers.
    """

    INIT_TIMEOUT = 5000
    max_velocity = Decimal(2.2)
    max_acceleration = Decimal(1.0)
    buffer = 0.5 # mm

    def __init__(self, serial_number,motor_type):
        self.serial_number = str(serial_number)
        self.motor_type = str(motor_type)

    def create(self):
        # abstract
        pass

    def get_device(self):
        try:
            device = self.device
        except AttributeError:
            print('device not created!')
            raise

        return device

    def enable(self):
        device = self.get_device()
        device.Connect(self.serial_number)
        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(self.INIT_TIMEOUT)
        device.StartPolling(POLLING_INTERVAL)
        time.sleep(ENABLE_SLEEP_TIME)
        device.EnableDevice()
        time.sleep(ENABLE_SLEEP_TIME)
        device.LoadMotorConfiguration(self.serial_number)
        
    def get_serial_number(self):
        device = self.get_device()
        device_info = device.GetDeviceInfo()
        return device_info.SerialNumber

    def get_homing_velocity(self):
        device = self.get_device()
        return device.GetHomingVelocity()
        
    def get_name(self):
        device = self.get_device()
        device_info = device.GetDeviceInfo()
        return device_info.Name

    def get_position(self):
        device = self.get_device()
        return Decimal.ToDouble(device.DevicePosition)

    def get_velocity(self):
        device = self.get_device()
        params = device.GetVelocityParams()
        velocity = Decimal.ToDouble(params.MaxVelocity)
        acceleration = Decimal.ToDouble(params.Acceleration)
        return velocity
        
    def set_velocity(self, velocity = max_velocity, acceleration = max_acceleration):
        device = self.get_device()
        device.SetVelocityParams(velocity, acceleration)
        
    def is_homed(self):
        device = self.get_device()
        return device.Status.IsHomed

    def home(self):
        device = self.get_device()
        device.SetHomingVelocity(max_velocity)
        device.Home(0)

    def stop(self):
        device = self.get_device()
        device.Stop(0)

    def max_range(self):
        if self.motor_type == "translation":
            return 25
        elif self.motor_type == "rotation":
            return 12
        else:
            print("not a valid motor type")

    def stop_immediate(self):
        device = self.get_device()
        device.StopImmediate()

    def velocity(self,vel,buffer=buffer):
        device = self.get_device()
        try:
            if vel < 0:
                if self.get_position() < self.buffer:
                    print("velocity negative")
                    print("position: {}, buffer: {}".format(self.get_position(),self.buffer))
                    print("Reached the bottom edge of the range")
                    self.stop_immediate()
                else:
                    device.MoveContinuousAtVelocity(MotorDirection.Backward,abs(vel))
            else:
                if self.get_position() > self.max_range()-self.buffer:
                    print("velocity positive")
                    print("position: {}, buffer: {}".format(self.get_position(),self.buffer))
                    print("Reached the top edge of the range")
                    self.stop_immediate()
                else:
                    device.MoveContinuousAtVelocity(MotorDirection.Forward,abs(vel))
        except Exception as e:
            print(e)
 
    def move_relative(self,dis):
        device = self.get_device()
        device.StopImmediate()
        device.SetMoveRelativeDistance(Decimal(dis))
        time.sleep(ENABLE_SLEEP_TIME)
        print("max range: {}, min range: {}".format(self.max_range()-self.buffer,self.buffer))
        print("requested position: {}".format(self.get_position()+dis))
        device.SetVelocityParams(self.max_velocity,self.max_acceleration)
        if self.get_position()+dis > self.max_range()-self.buffer:
            print("Move would result in invalid position")
        elif self.get_position()+dis < self.buffer:
            print("Move would result in invalid position")
        else:
            try:
                device.MoveRelative(0)
            except Exception as e:
                print(e)
            
    def move_absolute(self,pos):
        device = self.get_device()
        device.StopImmediate()
        params = device.GetVelocityParams()
        device.SetVelocityParams(self.max_velocity,self.max_acceleration)
        time.sleep(ENABLE_SLEEP_TIME)
        if (self.buffer < pos) and (pos < self.max_range()-self.buffer):
            try:
                device.MoveTo(Decimal(pos),0)
            except Exception as e:
                print(e)
        else:
            print("Move would result in invalid position")  

    def reset(self):
        device = self.get_device()
        try:
            self.disable()
        except Exception as e:
            print(e)
        try: 
            self.disconnect()
        except Exception as e:
            print(e)
        self.create() # these should happen every time, if there was an error or not
        self.enable()

    def get_status(self):
        device = self.get_device()
        return device.Status.IsMoving
        
    def disable(self):
        device = self.get_device()
        device.DisableDevice()

    def disconnect(self):
        device = self.get_device()
        device.Disconnect()

class KCubeMotor(Motor):

    """
    Base class for K-Cubes.
    """
        
    def set_joystickmode_velocity(self):
    
        device = self.get_device()
        params = device.GetMMIParams()
        try:
            # prior to kinesis 1.14.6
            params.WheelMode = Thorlabs.MotionControl.GenericMotorCLI.Settings.KCubeMMISettings.KCubeWheelMode.Velocity
        except AttributeError:
            try:
                params.JoystickMode = Thorlabs.MotionControl.GenericMotorCLI.Settings.KCubeMMISettings.KCubeJoystickMode.Velocity
            except AttributeError:
                raise AttributeError('cannot find this attribute. APIs have changed. look up latest documentation.')
        device.SetMMIParams(params)
        
    def set_display_intensity(self, intensity):
    
        device = self.get_device()
        params = device.GetMMIParams()
        params.DisplayIntensity = intensity
        device.SetMMIParams(params)
        
    def set_display_timeout(self, timeout):
    
        device = self.get_device()
        params = device.GetMMIParams()
        params.DisplayTimeout = timeout
        device.SetMMIParams(params)
    
        
class TCubeMotor(Motor):

    """
    Base class for K-Cubes.
    """

    pass
        
class KCubeDCServo(KCubeMotor):

    def create(self):
    
        clr.AddReference("ThorLabs.MotionControl.KCube.DCServoCLI")
        from Thorlabs.MotionControl.KCube.DCServoCLI import KCubeDCServo
        
        DeviceManagerCLI.BuildDeviceList()
        self.device = KCubeDCServo.CreateKCubeDCServo(self.serial_number)

class TCubeDCServo(TCubeMotor):

    def create(self):
    
        clr.AddReference("ThorLabs.MotionControl.TCube.DCServoCLI")
        from Thorlabs.MotionControl.TCube.DCServoCLI import TCubeDCServo

        DeviceManagerCLI.BuildDeviceList()
        self.device = TCubeDCServo.CreateTCubeDCServo(self.serial_number)
        
class TCubeStepper(TCubeMotor):

    def create(self):
        
        clr.AddReference("Thorlabs.MotionControl.TCube.StepperMotorCLI")
        from Thorlabs.MotionControl.TCube.StepperMotorCLI import TCubeStepper
        
        DeviceManagerCLI.BuildDeviceList()
        self.device = TCubeStepper.CreateTCubeStepper(self.serial_number)
