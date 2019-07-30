import unittest
import time

KINESIS_PATH = r'C:\Program Files\Thorlabs\Kinesis'
import py_thorlabs_ctrl.kinesis
py_thorlabs_ctrl.kinesis.init(KINESIS_PATH)
from py_thorlabs_ctrl.kinesis.motor import KCubeDCServo, TCubeDCServo, TCubeStepper

class TestMotor(unittest.TestCase):

    # T-Cube DCServo, K-Cube DCServo, T-Cube DCStepper
    MOTORS = [#(TCubeDCServo, 83854669),
        #(KCubeDCServo, 27502878),]
        (TCubeStepper, 80864431)]

    MOVE_ABS = 3
    MOVE_REL = -1.3
    ENABLE_WAIT = 2
    MOVE_WAIT = 10
    HOME_WAIT = 30
    
    
    def setUp(self):
    
        self.motors = []

        for motor_settings in self.MOTORS:
            motor = motor_settings[0](motor_settings[1])
            motor.create()
            motor.enable()
            time.sleep(self.ENABLE_WAIT)
            self.motors.append(motor)
    
    @unittest.skip("looks like SN getter is unreliable.")
    def test_0_test_sn(self):
    
        for idx, motor in enumerate(self.motors):
                
            serial_number = motor.get_serial_number()
            self.assertEqual(self.MOTORS[idx][1], serial_number)
            
    def test_1_test_move_home(self):
    
        for motor in self.motors:
            motor.home()
        
        time.sleep(self.HOME_WAIT)
        
        for motor in self.motors:
            is_homed = motor.is_homed()
            self.assertTrue(is_homed)
            
            pos = motor.get_position()
            self.assertAlmostEqual(pos, 0, 3)
        
    def test_2_test_move_absolute(self):

        for motor in self.motors:
            motor.move_absolute(self.MOVE_ABS)
            
        time.sleep(self.MOVE_WAIT)
        
        for motor in self.motors:
            pos = motor.get_position()
            self.assertAlmostEqual(pos, self.MOVE_ABS, 3)

    def test_3_test_move_relative(self):
    
        # should come after test 1
        
        for motor in self.motors:
            motor.move_relative(self.MOVE_REL)
        
        time.sleep(self.MOVE_WAIT)
            
        for motor in self.motors:
            pos = motor.get_position()
            self.assertAlmostEqual(pos, self.MOVE_ABS + self.MOVE_REL, 3)
            
    def tearDown(self):
    
        for motor in self.motors:
            
            motor.disable()
            motor.disconnect()

if __name__ == '__main__':
           
    unittest.main()