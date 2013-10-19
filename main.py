from ga import *


def main():
    ga = GeneticAlgorithm(Chromosome(Gene(0xffffff)), 20, 10, 85)
    
    a = ga.run()
    print(a)
    #print([x.encode() for x in ga.population])

if __name__ == '__main__':
    main()