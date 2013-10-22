from ga import *
import png

def main():
    #also needs to input a fitnessfunction into GA
    ga = GeneticAlgorithm(Chromosome(0x0f, 0xf0, 0x0f), 20, 0.005, 0.9) 

    result = ga.run()
    #print(result)

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
