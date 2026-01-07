#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

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
from vex import Motor, DirectionType, RotationUnit, port
def Move(speed, speed2):
    LeftMotor.set_velocity(speed, PERCENT)
    RightMotor.set_velocity(speed2, PERCENT)
    LeftMotor.spin(FORWARD)
    RightMotor.spin(REVERSE)
def Turn(NewAngle):
    if (Newangle>Headingtot):
        while (Headingtot>Newangle):
            Move(60,40)
        LeftMotor.stop()
        RightMotor.stop()
    if (Headingtot>Newangle):
        while (Headingtot<Newangle):
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
            if (x< & x> & y< & y>):
                dlist.append(distance)
            else:
                dlist.append(99999999999999999999999999999999999)
        tar=dlist.min()
        target=dlist.indexof(tar)
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
# Begin project cod
def cord_calc():
    Pi = 3.1415926535897932384626433
    global deltax = 0
    global deltay = 0
    #Reset the damn relative position#
    distancetot = 0
    DistanceLeft = ((3.25*Pi)/360)*(LeftMotor.position())
    DistanceRight = ((3.25*Pi)/360)*(RightMotor.position())
    DistanceMiddle = ((3.25*Pi)/360)*(MiddleMotor.position())
    global Headingtot = (DistanceRight-DistanceLeft)/2
    r = ((90/Headingtot)*(DistanceLeft+DistanceRight))/Pi
    alpha = Pi-Heading
    Distancetot = (DistanceLeft+DistanceRight)/2
    y = (math.sin(Headingtot)*r)
    deltax = (r-(math.cos(Headingtot)*r))+DistanceMiddle
    deltay = (math.sin(Headingtot))
    return deltax, deltay
def main():
    
main()
#WRITE MAIN CODE UNDER HERE#

    



    
