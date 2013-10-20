from ga import *
import png

def main():

    # a = Chromosome("hello world")
    # print(a.decode())

    #also needs to input a fitnessfunction into GA
    ga = GeneticAlgorithm(Chromosome(0xff), 20, 0.05, 0.8) 

    result = ga.run()
    #print(result)

    pixels = []
    for x in result:
        pixelrow = []
        for y in x:
            pixelrow.append(0)
            pixelrow.append(y[0])
            pixelrow.append(0)
            # y = list(y)
            # while len(y) < 24:
            #     y = ['0'] + y
            # y = "".join(y)
            # pixelrow.append(int(y[0:7],2))
            # pixelrow.append(int(y[8:15],2))
            # pixelrow.append(int(y[16:23],2))

        pixels.append(tuple(pixelrow))

    f = open('swatch.png', 'wb')
    w = png.Writer(20, len(pixels))
    w.write(f, pixels) ; f.close()

if __name__ == '__main__':
    main()