import os, sys, clr

THORLABS_KINESIS_CONTROL_DLL_FILENAME = 'Thorlabs.MotionControl.Controls.dll'

this = sys.modules[__name__]
this.PATH_SET = False

def init(path):

    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, THORLABS_KINESIS_CONTROL_DLL_FILENAME)):
            sys.path.append(path)
            this.PATH_SET = True
        else:
            raise ImportError('Cannot find .NET controls')
    else:
        raise ImportError('Path does not exist')
        
    clr.AddReference('System.Collections')

    clr.AddReference("Thorlabs.MotionControl.Controls")
    import Thorlabs.MotionControl.Controls

def check_import():
    if not this.PATH_SET:
        raise ImportError('Must initialize before importing this package. Use py_thorlabs_ctrl.kinesis.init(path)')