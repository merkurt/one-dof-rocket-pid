class PID(object):
    def __init__(self, kp, ki, kd, timeStep, integralErrorMax):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.timeStep = timeStep
        self.integralErrorMax = integralErrorMax
        self.error = 0
        self.lastError = 0
        self.integralError = 0

    def calculate(self, currentPosition, targetPosition):
        self.error = targetPosition - currentPosition
        
        #calculate proportional term
        pTerm = self.Kp * self.error

        #calculate integral term with limiting
        self.integralError = self.integralError + (self.error * self.timeStep)
        if(self.integralError > self.integralErrorMax):
            self.integralError = self.integralErrorMax
        elif(self.integralError < ((-1) * self.integralErrorMax)):
            self.integralError = (-1) * self.integralErrorMax
        #!duruma göre min degerini de ekle
        iTerm = self.Ki * (self.integralError)

        #calculate derivative term
        dTerm = self.Kd * ((self.error - self.lastError) / self.timeStep)

        self.lastError = self.error

        return pTerm + iTerm + dTerm