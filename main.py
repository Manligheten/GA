from ga import *
import png

def main():
    ga = GeneticAlgorithm(goal = Chromosome(0x00, 0x00, 0x00), popsize = 20, 
            mutrate = 0.05, crossrate = 0.75, fitnessFunc = fitColours,
            maxFitness = maxFitnessColours)

    result = ga.run()

    pixels = []
    for x in result:
        pixelrow = []
        for y in x:
            pixelrow.append(y[0])
            pixelrow.append(y[1])
            pixelrow.append(y[2])

        pixels.append(tuple(pixelrow))

    f = open('swatch.png', 'wb')
    w = png.Writer(20, len(pixels))
    w.write(f, pixels) ; f.close()

if __name__ == '__main__':
    main()
