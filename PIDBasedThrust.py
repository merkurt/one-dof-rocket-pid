from PID import *

class PIDBasedThrust(object):
    def __init__(self, min, max, kp, ki, kd, timeStep, integralErrorMax):
        self.min = min
        self.max = max
        self.thrustArray = list()
        self.pid = PID(kp, ki, kd, timeStep, integralErrorMax)

    def thrust(self, currentPosition, targetPosition):
        thrust = self.pid.calculate(currentPosition, targetPosition)
        if(thrust > self.max):
            thrust = self.max
        elif(thrust < self.min):
            thrust = self.min
        self.thrustArray.append(thrust)
        return thrust