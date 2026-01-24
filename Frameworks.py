#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
MiddleMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
LeftMotor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
RightMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
ClampMotor = Motor29(brain.three_wire_port.a, False)
BaseMotor = Motor29(brain.three_wire_port.b, False)
ElbowMotor = Motor29(brain.three_wire_port.c, False)
BasePot = Potentiometer(brain.three_wire_port.d)
ElbowPot = Potentiometer(brain.three_wire_port.e)
controller_2 = Controller(PARTNER)


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
# Project:      VEXcode Project
# Author:       VEX
# Created:
# Description:  VEXcode V5 Python Project
#
# ------------------------------------------

# Library imports
from vex import Motor, DirectionType
Pi = 3.1415926535897932384626433
x1=10.0
y1=10.0
pB = 0.6
pE = 0.6
iB = 0.6
iE = 0.6
dB = 0.6
dE = 0.6
def IK_calc(x, y):
    SE = 10
    EG = 10
    c = math.sqrt(x**2+y**2)
    EAngle = ((math.acos(SE**2+EG**2-c**2))/(2*SE*EG))*(180/Pi)
    SAngle = ((math.acos(SE**2+c**2-EG**2))/(2*SE*c))*(180/Pi)
    return EAngle, SAngle
def Move(speed, speed2):
    LeftMotor.set_velocity(speed, PERCENT)
    RightMotor.set_velocity(speed2, PERCENT)
    LeftMotor.spin(FORWARD)
    RightMotor.spin(REVERSE)
def Turn(NewAngle):
    if (NewAngle>Headingtot):
        while (Headingtot>NewAngle):
            Move(60,40)
        LeftMotor.stop()
        RightMotor.stop()
    if (Headingtot>NewAngle):
        while (Headingtot<NewAngle):
            Move(40,60)
        LeftMotor.stop()
        RightMotor.stop()
def Coordinate(x, y, angle):
    tot=12
    distance=360
    while(x<x+1 & x>x-1):
        x,y = cord_calc()
        dlist=[1]
        for n in range (12):
            ntheta= (n-1)*(360/tot)+ntheta
            pointx=math.cos(ntheta)
            pointy=math.sin(ntheta)
            distance=math.sqrt(((x-pointx)**2)+((y-pointy)**2))
            if (x<4 & x>5 & y<8 & y>2):
                dlist.append(distance)
            else:
                dlist.append(999999999999999999999999999999999999)
        tar=min(dlist)
        target=dlist.index(tar)
        tarangle=(target-1)*(360/tot)
        Turn(tarangle)
        LeftMotor.spin_for(FORWARD, distance, DEGREES, wait=False)
        RightMotor.spin_for(FORWARD, distance, DEGREES)
        if (x<x+5 & x>x-5 & y<y+5 & y>y-5):
            break
       
    angy = math.atan((x-deltax)/(y-deltay))*(180/Pi)
    Turn(angy)
   
    while((deltax<x+1 & deltax>x-1)==False):
        Move(100,100)

    LeftMotor.stop()
    RightMotor.stop()
   
    if (angle>Headingtot):
        while (Headingtot>angle):
            Move(60,40)
        LeftMotor.stop()
        RightMotor.stop()
    if (Headingtot>angle):
        while (Headingtot<angle):
            Move(40,60)
        LeftMotor.stop()
        RightMotor.stop()
def cord_calc():
    global deltay, deltax, Headingtot
    deltax = 0
    deltay = 0
    #Reset the damn relative position#
    distancetot = 0
    axletrack = 8.25
    DistanceLeft = ((3.25*Pi)/360)*(LeftMotor.position())
    DistanceRight = ((3.25*Pi)/360)*(RightMotor.position())
    DistanceMiddle = ((3.25*Pi)/360)*(MiddleMotor.position())
    Headingtot = (DistanceRight-DistanceLeft)/2+0.001
    r = ((90/Headingtot)*(DistanceLeft+DistanceRight))/Pi
    c = 2*(DistanceRight/Headingtot+(axletrack/2))*(math.sin(Headingtot/2))
    Distancetot = (DistanceLeft+DistanceRight)/2
    deltax = ((math.cos((Pi-Headingtot)/2)*c))+DistanceMiddle
    deltay = (math.sin(Headingtot)*r)
    return deltax, deltay

LeftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
RightMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
MiddleMotor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)

wait(30, MSEC)

def deadzone(value):
    if abs(value) < 5:
        value = 0
    return value

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def exp_ramp(current, target, gain):
    return current + (target - current) * gain

def snap(value, threshold=1):
    return 0 if abs(value) < threshold else value

RAMP_GAIN = 0.2   # 0 < gain < 1

current_left = 0
current_right = 0
current_horiz = 0

while True:

    MAX_SPEED = 80
    SPEED_STEP = 10

    # Read joysticks
    vert_movement = deadzone(controller_1.axis2.position())
    horiz_movement = deadzone(controller_1.axis1.position())
    turn_amount = deadzone(controller_1.axis4.position())

    if controller_1.buttonUp.pressing():
        MAX_SPEED += SPEED_STEP
        wait(200, MSEC)

    if controller_1.buttonDown.pressing():
        MAX_SPEED -= SPEED_STEP
        wait(200, MSEC)


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
    target_horiz = clamp(target_horiz, -100, 100)


    # Smooth acceleration
    current_left = exp_ramp(current_left, target_left, RAMP_GAIN)
    current_right = exp_ramp(current_right, target_right, RAMP_GAIN)
    current_horiz = exp_ramp(current_horiz, target_horiz, RAMP_GAIN)

    # Smooth stops
    current_left = snap(current_left)
    current_right = snap(current_right)
    current_horiz = snap(current_horiz)

    # Apply speeds
    LeftMotor.set_velocity(current_left, PERCENT)
    RightMotor.set_velocity(current_right, PERCENT)
    MiddleMotor.set_velocity(current_horiz, PERCENT)

    LeftMotor.spin(FORWARD)
    RightMotor.spin(FORWARD)
    MiddleMotor.spin(FORWARD)
    if (controller_2.buttonR1.pressed):
        ClampMotor.set_velocity(50, PERCENT)
        ClampMotor.spin(FORWARD)
    elif (controller_2.buttonR1.released):
        ClampMotor.stop()
    if (controller_2.buttonL1.pressed):
        ClampMotor.set_velocity(-50, PERCENT)
        ClampMotor.spin(FORWARD)
    elif (controller_2.buttonL1.released):
        ClampMotor.stop()    

    if (controller_2.buttonUp.pressing()):
        y1 = y1 + 0.1
        wait(5, MSEC)
    if (controller_2.buttonDown.pressing()):
        y1 = y1 - 0.1
        wait(5, MSEC)
    if (controller_2.buttonRight.pressing()):
        x1 = x1 + 0.1
        wait(5, MSEC)
    if (controller_2.buttonLeft.pressing()):
        x1 = x1 - 0.1
        wait(5, MSEC)
    IK_calc(x1, y1) = angle2, angle1
    CBangle = BasePot.angle()
    CEangle = ElbowPot.angle()
    if (CBangle>(angle1-5) && CBangle<(angle+5)):
        Berror = 0
    else:
        Berror = (CBangle-angle1)*(11/36)
    if (CEangle>(angle2-5) && CEangle<(angle2+5)):
        Eerror = 0
    else:
        Eerror = (CEangle-angle2)*(11/36)
    Bspeed = pB*Berror
    Espeed = pE*Eerror
    BaseMotor.set_velocity(Bspeed, PERCENT)
    ElbowMotor.set_velocity(Espeed, PERCENT)
    brain.screen.print(cord_calc() + "Max Speed: ", MAX_SPEED)
    brain.screen.next_row()
    wait(20, MSEC)
