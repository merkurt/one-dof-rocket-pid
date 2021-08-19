import turtle
from PIDBasedThrust import *
from plotter import *

#global params
PI = 3.14159
GRAM_TO_KG = 1 / 1000
GRAVITY = 9.80665 # m/s^2
RHO = 1.225

#simulation
PID_STATUS = 1 # on:1 off:0
TARGET_POINT = 100
START_POINT_X = 0
START_POINT_Y = -100
SETPOINT = TARGET_POINT - START_POINT_Y

#time
SIM_TIME = 20
TIME_STEP = 0.05

#PID
#https://en.wikipedia.org/wiki/Ziegler–Nichols_method
ku = 0.5
tu = 20
KP = 0.6 * ku
KI = (1.2 * ku) / tu
KD = 0.075 * ku * tu
INTEGRAL_ERROR_MAX = 400

#physics
MAX_THRUST = 50
MIN_THRUST = 0
THRUST_TIME = 2.5 # -1 for PID
CD = 0.5
DIAMETER = 0.04 #m
MASS = 1000 #grams
INITIAL_A = 0
INITIAL_V = 0
INITIAL_H = 0

class Simulation(object):
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.rocket = Rocket(MASS, CD, DIAMETER)
        self.marker = turtle.Turtle()
        self.marker.penup()
        self.marker.speed(10)
        self.marker.left(180)
        self.marker.goto(15, TARGET_POINT)
        self.marker.color("red")
        self.simTimer = 0
        self.simStatus = True
        self.timeArray = list()

    def run(self):
        while(self.simStatus):
            self.simTimer += TIME_STEP
            self.timeArray.append(self.simTimer)
            #cycle start
            if(PID_STATUS):
                self.simStatus = self.rocket.updatePIDBased(SETPOINT)
            else:
                self.simStatus = self.rocket.updateTimeBased(self.simTimer)
            #cycle end
            if(self.simTimer > SIM_TIME):
                self.simStatus = False

class Rocket(object):
    def __init__(self, mass, cd, dia):
        ##object
        #body
        self.Rocket = turtle.Turtle()
        self.Rocket.shape("square")
        self.Rocket.color('black')
        self.Rocket.penup()
        self.Rocket.goto(START_POINT_X, START_POINT_Y)
        self.Rocket.speed(0)
        self.colorList = ['black', 'green', 'blue', 'red']
        self.color = 0 # 0:black, 1:green, 2:blue, 3:red
        #motor
        if(PID_STATUS):
            self.motor = PIDBasedThrust(MIN_THRUST, MAX_THRUST, KP, KI, KD, TIME_STEP, INTEGRAL_ERROR_MAX)
        else:
            self.motor = Thrust(MIN_THRUST, MAX_THRUST, THRUST_TIME)
        #physics
        self.cd = cd
        self.surface_area = PI * dia * dia
        self.mass = mass
        self.ddy = INITIAL_A
        self.ddyArray = list()
        self.dy = INITIAL_V
        self.dyArray = list()
        self.y = INITIAL_H
        self.yArray = list()
        #status
        self.done = 0
    
    def calculateDynamicPressure(self, velocity):
        return 0.5 * RHO * velocity**2      #RHO atmosfer modelinden sonra disaridan beslenebilir

    def calculateDrageForce(self, velocity):
        return self.calculateDynamicPressure(velocity) * self.surface_area * self.cd

    def setAcceleration(self, thrust):
        """
        f = m*a -> a_thust = f_thrust / m_total, a_total = a_thrust - a_drag - a_gravity 
        """
        if(thrust > 0):
            self.color = 1
        else:
            self.color = 2
        self.ddy = (thrust - self.calculateDrageForce(self.dy)) / (self.mass * GRAM_TO_KG) - GRAVITY
        self.ddyArray.append(self.ddy)

    def getAcceleration(self):
        return self.ddy

    def setVelocity(self):
        self.dy = self.dy + (self.getAcceleration() * TIME_STEP)
        self.dyArray.append(self.dy)
        if self.dy < 0:
            self.color = 3

    def getVelocity(self):
        return self.dy

    def setPosition(self):
        if(self.y >= INITIAL_H):
            self.y = self.y + (self.getVelocity() * TIME_STEP)
        else:
            self.color = 0
            self.done = 1
        self.yArray.append(self.y)
        print("altitude:", self.y)
        self.Rocket.sety(self.y + START_POINT_Y)
    
    def getPosition(self):
        return self.y
    
    def setColor(self):
        self.Rocket.color(self.colorList[self.color])
    
    def updateTimeBased(self, time):
        self.setAcceleration(self.motor.thrust(time))
        self.setVelocity()
        self.setPosition()
        self.setColor()
        return not self.done
    
    def updatePIDBased(self, target):
        thrust = self.motor.thrust(self.getPosition(), target)
        self.setAcceleration(thrust)
        self.setVelocity()
        self.setPosition()
        if(thrust > 0):
            self.color = 1
        self.setColor()
        return not self.done

class Thrust(object):
    def __init__(self, minT, maxT, duration):
        self.min = minT
        self.max = maxT
        self.duration = duration
        self.thrustArray = list()
    
    def thrust(self, time):
        if(time <= self.duration):
            self.thrustArray.append(self.max)
        else:
            self.thrustArray.append(self.min)
        return self.thrustArray[-1]

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
    plot1(sim.timeArray, sim.rocket.motor.thrustArray, sim.rocket.ddyArray, sim.rocket.dyArray, sim.rocket.yArray)
