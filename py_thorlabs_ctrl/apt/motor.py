
class Motor:

    """
    For use with legacy (APT) ActiveX controls in Qt (i.e. PyQt5 -- activeQt, QAxWidget)
    """

    serial_number = ''
    device = None

    def __init__(self, serial_number):
        self.serial_number = str(serial_number)
        
    def set_activex_ctrl(self, ctrl):

        ctrl.setControl('MGMOTOR.MGMotorCtrl.1')
        ctrl.setProperty('HWSerialNum', self.serial_number)

        self.device = ctrl

    def create(self):
        pass

    def get_device(self):
        try:
            device = self.device
        except AttributeError:
            print("device not created!")
            raise

        return device

    def enable(self):
        device = self.get_device()

        device.dynamicCall('StartCtrl')

    def disable(self):
        device = self.get_device()
        
        device.dynamicCall('StopCtrl')
        
    def is_homed(self):
    
        HOMED_BIT = 10
        
        device = self.get_device()
        status = device.GetStatusBits_Bits(0) + 1 << 31
        return bool((status >> HOMED_BIT) % 2)
        
    def home(self):
    
        device = self.get_device()
        device.MoveHome(0, 0)

    def get_position(self):
        device = self.get_device()

        pos = float(device.dynamicCall('GetPosition_Position(0)'))

        return pos

    def move_relative(self, dis):
        device = self.get_device()

        move_str = 'SetRelMoveDist(0, %.2f)' % dis

        device.dynamicCall(move_str)
        device.dynamicCall("MoveRelative(0, false)")

    def move_absolute(self, pos):


        device = self.get_device()

        move_str = 'SetAbsMovePos(0, %.2f)' % pos

        device.dynamicCall(move_str)
        device.dynamicCall('MoveAbsolute(0, false)')
