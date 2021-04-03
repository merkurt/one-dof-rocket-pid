import turtle
from plotter import *

#global params
PI = 3.14159
GRAM_TO_KG = 1 / 1000
GRAVITY = 9.80665 # m/s^2
RHO = 1.225

#simulation
SETPOINT = 100
START_POINT_X = 0
START_POINT_Y = -100

#time
SIM_TIME = 30
TIME_STEP = 0.05

#physics
MAX_THRUST = 25
MIN_THRUST = 0
THRUST_TIME = 2.5
CD = 0.5
DIAMETER = 0.02 #m
MASS = 600 #grams
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
        self.marker.goto(15, SETPOINT)
        self.marker.color("red")
        self.simTimer = 0
        self.simStatus = True
        self.timeArray = list()

    def run(self):
        while(self.simStatus):
            self.simTimer += TIME_STEP
            self.timeArray.append(self.simTimer)
            #cycle start
            self.simStatus = self.rocket.update(self.simTimer)
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
        aThrust = (thrust - self.calculateDrageForce(self.dy)) / (self.mass * GRAM_TO_KG)
        self.ddy = aThrust - GRAVITY
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
        self.Rocket.sety(self.y + START_POINT_Y)
    
    def getPosition(self):
        return self.y
    
    def setColor(self):
        self.Rocket.color(self.colorList[self.color])
    
    def update(self, time):
        self.setAcceleration(self.motor.thrust(time))
        self.setVelocity()
        self.setPosition()
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
