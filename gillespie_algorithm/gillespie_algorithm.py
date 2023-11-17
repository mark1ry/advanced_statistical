import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

from realization import Realization


def createEnsamble(preyBirthRate, hawkHuntingRate, hawkDeatRate, initialHawks,
                   initialPrey, maximumTime, timeStepSize, ensambleSize):
    ensamble = [Realization(preyBirthRate, hawkHuntingRate, hawkDeatRate) for instance in range(ensambleSize)]
    for instance in ensamble:
        instance.gillespieSimulation(initialHawks, initialPrey, maximumTime)
        instance.convertToRegularSteps(maximumTime, timeStepSize)
    return ensamble

def calculateEnsambleMean(ensamble, ensambleSize):
    ensambleSum = np.zeros((3, ensamble[0].getNumberOfTimeSteps()))
    for instance in ensamble:
        realizationSequence = instance.getRealization()
        realizationSequence = np.array(realizationSequence)
        ensambleSum += realizationSequence
    
    ensambleSum /= ensambleSize
    return ensambleSum
      
def plotExtendedFigure (gillespieEnsamble, ensambleSize, lotkaVolterraEnsamble, *args):
    plt.figure(figsize=(12, 18))
    index = 1
    for size in [1, 10, 50, 100, ensambleSize]:
        ax = plt.subplot(3, 2, index)
        timeGillespie, hawksGillespie, preyGillespie = calculateEnsambleMean(gillespieEnsamble[:size], size)
        plotAx(ax, timeGillespie, hawksGillespie, preyGillespie, size, args[0], args[1], args[2])
        index += 1
    
    plt.subplot(3, 2, 6)
    timeLotkaVolterra, hawksLotkaVolterra, preyLotkaVolterra = lotkaVolterraEnsamble.getRealization()
    plt.plot(timeLotkaVolterra, preyLotkaVolterra, label="Prey")
    plt.plot(timeLotkaVolterra, hawksLotkaVolterra, label="Predator")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.legend(loc='upper left')
    plt.title("Lotka-Volterra Simulation")
    plt.xlim(0, max(timeLotkaVolterra))
    plt.ylim(0, 1.1*max(max(preyLotkaVolterra),max(hawksLotkaVolterra)))

    plt.tight_layout()
    plt.savefig(f"output_example/figure_r{args[0]}_b{args[1]}_d{args[2]}_extended.png")
    plt.show()    
    
def plotInSameAx(gillespieEnsamble, ensambleSize, lotkaVolterraEnsamble, *args):
    
    timeGillespie, hawksGillespie, preyGillespie = calculateEnsambleMean(gillespieEnsamble, ensambleSize)
    timeLotkaVolterra, hawksLotkaVolterra, preyLotkaVolterra = lotkaVolterraEnsamble.getRealization()
    plt.figure(figsize=(8, 5))
    ax = plt.subplot(1, 1, 1)
    ax.plot(timeGillespie, preyGillespie, '-', label="Prey Gillespie")
    ax.plot(timeGillespie, hawksGillespie, '-', label="Predator Gillespie")
    ax.plot(timeLotkaVolterra, preyLotkaVolterra, '--', label="Prey Lotka-Volterra")
    ax.plot(timeLotkaVolterra, hawksLotkaVolterra, '--', label="Predator Lotka-Volterra")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.legend(loc='upper left')
    plt.title("Gillespie Ensamble vs Lotka-Volterra")
    text_str = f"r= {args[0]}, $\\beta$ = {args[1]}, d = {args[2]}, N = {ensambleSize}"
    anchored_text = AnchoredText(text_str, loc='upper right', frameon=True)
    plt.gca().add_artist(anchored_text)
    plt.xlim(0, max(timeLotkaVolterra))
    plt.ylim(0, 1.1*max(max(preyLotkaVolterra),max(hawksLotkaVolterra), max(hawksGillespie), max(preyGillespie)))

    plt.tight_layout()
    plt.savefig(f"output_example/figure_r{args[0]}_b{args[1]}_d{args[2]}_compact.png")
    plt.show()
   
def plotAx(ax, time, hawks, prey, ensambleSize, *args):
    ax.plot(time, prey, label="Prey")
    ax.plot(time, hawks, label="Predator")
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.legend(loc='upper left')
    ax.set_title("Gillespie Simulation Ensamble Average")
    text_str = f"r= {args[0]}, $\\beta$ = {args[1]}, d = {args[2]}, N = {ensambleSize}"
    anchored_text = AnchoredText(text_str, loc='upper right', frameon=True)
    plt.gca().add_artist(anchored_text)
    # Set the axes' limits
    plt.xlim(0, max(time))
    plt.ylim(0, 1.1*max(max(hawks),max(prey)))

 
def main ():
    ensambleSize = 1500
    
    preyBirthRate = 0.5
    predationRate = 0.01
    hawkDeathRate = 0.25
    
    initialHawkPopoulation = 20
    initialPreyPopulation = 50
    maximumTime = 35
    timeStep = 0.2


    gillespieEnsamble = createEnsamble(preyBirthRate, predationRate, hawkDeathRate, initialHawkPopoulation,
                                       initialPreyPopulation, maximumTime, timeStep, ensambleSize)
    print("Ensamble has been created")
    lotkaVolterraApproximation = Realization(preyBirthRate, predationRate, hawkDeathRate)
    lotkaVolterraApproximation.lotkaVolterraSimulation(initialHawkPopoulation, initialPreyPopulation, maximumTime, timeStep)
    print("Started plotting")
    plotExtendedFigure(gillespieEnsamble, ensambleSize, lotkaVolterraApproximation,
               preyBirthRate, predationRate, hawkDeathRate)
    plotInSameAx(gillespieEnsamble, ensambleSize, lotkaVolterraApproximation,
               preyBirthRate, predationRate, hawkDeathRate)
    
    return

if __name__ == "__main__":
    main()



