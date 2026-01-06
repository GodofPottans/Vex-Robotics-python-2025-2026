#region VEXcode Generated Robot Configuration

# Brain should be defined by default
brain=Brain()

# Robot configuration code
LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
MiddleMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
import urandom
import math

from vex import Motor, DirectionType, RotationUnit, port

# Begin project code

brain = Brain()
controller = Controller()


LeftMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
MiddleMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)

wait(30, MSEC)

def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))

def deadzone(value):
    if abs(value) < 5:
        return 0
    return value

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def ramp(current, target, rate):
    if target > current + rate:
        return current + rate
    elif target < current - rate:
        return current - rate
    else:
        return target

RAMP_RATE = 8   # how fast the speed can change each loop

current_left = 0
current_right = 0
current_strafe = 0

while True:

    MAX_SPEED = 80

    # Read joysticks
    vert_movement = deadzone(controller.axis2.position())
    horiz_movement = deadzone(controller.axis1.position())
    turn_amount = deadzone(controller.axis3.position())

    # Scale speed
    vert_movement = vert_movement * MAX_SPEED / 100
    horiz_movement = horiz_movement * MAX_SPEED / 100
    turn_amount = turn_amount * MAX_SPEED / 100

    # Target motor speeds
    target_left = vert_movement + turn_amount
    target_right = vert_movement - turn_amount
    target_horiz = horiz_movement

    # Prevent speeds from exeeding +-100%
    target_left = clamp(target_left, -100, 100)
    target_right = clamp(target_right, -100, 100)
    target_horiz = clamp(target_strafe, -100, 100)


    # Smooth acceleration
    current_left = ramp(current_left, target_left, RAMP_RATE)
    current_right = ramp(current_right, target_right, RAMP_RATE)
    current_horiz = ramp(current_horiz, target_horiz, RAMP_RATE)

    # Apply speeds
    LeftMotor.set_velocity(current_left, PERCENT)
    RightMotor.set_velocity(current_right, PERCENT)
    MiddleMotor.set_velocity(current_horiz, PERCENT)

    LeftMotor.spin(FORWARD)
    RightMotor.spin(FORWARD)
    MiddleMotor.spin(FORWARD)

    wait(20, MSEC)

