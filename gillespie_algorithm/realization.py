import numpy as np


class Realization:
    def __init__(self, preyBirthRate, hawkHuntingRate, hawkDeathRate):
        self.timeOfEvent = []
        self.hawkNumber = []
        self.preyNumber = []

        self.preyBirthRate = preyBirthRate
        self.hawkHuntingRate = hawkHuntingRate
        self.hawkDeathRate = hawkDeathRate

    def gillespieSimulation(self, initialHawks, initialPrey, timeLimit):
        # Initialize simulation parameters
        currentTime = 0
        hawks = initialHawks
        prey = initialPrey

        self.timeOfEvent = [currentTime,]
        self.hawkNumber = [hawks,]
        self.preyNumber = [prey,]
        
        # Main simulation loop
        while currentTime < timeLimit:
            # Calculate rates of events (you may need to replace these with your specific model)
            preyBirthRate = self.preyBirthRate * prey
            hawkHuntingRate = self.hawkHuntingRate * prey * hawks
            hawkDeathRate = self.hawkDeathRate * hawks

            totalRate = preyBirthRate + hawkHuntingRate + hawkDeathRate
            
            if totalRate <= 0:
                timeUntilNextEvent = 0.02
            else:  
                # Calculate time until the next event
                timeUntilNextEvent = -np.log(np.random.rand()) / totalRate

                # Update system state based on the chosen event
                randomNumber = np.random.rand()

                if randomNumber < preyBirthRate/totalRate:
                    prey += 1
                elif randomNumber < (preyBirthRate + hawkHuntingRate)/totalRate:
                    prey -= 1
                    hawks += 1
                else:
                    hawks -= 1
                
            # Update time and record state
            currentTime += timeUntilNextEvent
            self.timeOfEvent.append(currentTime)
            self.hawkNumber.append(hawks)
            self.preyNumber.append(prey)

        
    def getRealization(self):

        return self.timeOfEvent, self.hawkNumber, self.preyNumber

    def getState(self, time):
        index = 0
        for element in self.timeOfEvent:
            if element >= time:
                return self.hawkNumber[index-1], self.preyNumber[index-1]
            index += 1
        
        
    """
    convertToRegularSteps (self, int stepsize)

        In order to calculate the averege of the ensamble, we need to compute
        the ensamble averege at different times. Because the time steps in the
        process are random, this function finds the state of the system at regular
        steps in time.

    """
    def convertToRegularSteps(self, stepsize):

        regularHawksNumber = []
        regularPreyNumber = []
        regularTime = [time/10 for time in range(301)]
        
        for currentTimeStep in regularTime:
            if currentTimeStep == 0:
                regularHawksNumber.append(self.hawkNumber[0])
                regularPreyNumber.append(self.preyNumber[0])
            else:
                regularHawksNumber.append(self.getState(currentTimeStep)[0])
                regularPreyNumber.append(self.getState(currentTimeStep)[1])

        self.hawkNumber = regularHawksNumber
        self.preyNumber = regularPreyNumber
        self.timeOfEvent = regularTime

    def getNumberOfTimeSteps(self):
        
        length = 0
        for element in self.timeOfEvent:
            length += 1
        
        return length
    
    def lotkaVolterraSimulation(self, initialHawks, initialPrey, timeLimit, timeStep):
        
        currentTime = 0
        hawks = initialHawks
        prey = initialPrey

        self.timeOfEvent = [currentTime,]
        self.hawkNumber = [hawks,]
        self.preyNumber = [prey,]
        
        while currentTime < timeLimit:
            preyChange = (self.preyBirthRate * prey - self.hawkHuntingRate * prey * hawks) * timeStep
            hawkChange = (self.hawkHuntingRate * prey * hawks - self.hawkDeathRate * hawks) * timeStep
            hawks += hawkChange
            prey += preyChange
            currentTime += timeStep
            
            self.timeOfEvent.append(currentTime)
            self.hawkNumber.append(hawks)
            self.preyNumber.append(prey)
