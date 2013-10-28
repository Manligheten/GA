import random
from collections import deque
from functools import partial

basetwo = partial(int, base=2)

def maxFitnessColours(obj):
    goal = obj.goal.bitstring()

    maxFitness = 0.0
    maxFitnessCount = 8
    for i, x in enumerate(goal):
        maxFitness += 1.0*maxFitnessCount
        maxFitnessCount -=1
        if i % 8 == 0:
            maxFitnessCount = 8

    return maxFitness

def fitColours(obj):
    goal = obj.goal.bitstring()

    for ch in obj.population:
        bitstring = deque(ch.bitstring())

        fitness = 0.0
        count = 8
        for i, x in enumerate(bitstring):
            if bitstring[i] == goal[i]:
                fitness += 1.0*count
                count -= 1
            if i % 8 == 0:
                count = 8

        ch.fitness = fitness/obj.maxFitness


class GAException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Chromosome():

    def __init__(self, *genotype):
        self.fitness = 0

        self.bitlist = []
        self.types = []

        self.encode(genotype)        

    def encode(self, genotype):
        enc = ""

        if isinstance(genotype[0], (tuple, list)):
            genotype = genotype[0]
        for gene in genotype:
            if isinstance(gene, int):
                enc = bin(gene)[2:]
            elif isinstance(gene, float):
                raise GAException("Not yet supported")
                # check struct etc...
            elif isinstance(gene, str):
                for c in gene:
                    tmp = deque(bin(ord(c))[2:])
                    while len(tmp) < 8:
                        tmp.appendleft('0')
                    tmp.appendleft(enc)
                    enc = "".join(tmp)
            
            self.bitlist.append(enc)
            self.types.append(type(gene))

    def decode(self):
        decoded = []
        for i, t in enumerate(self.types):
            if t == int:
                decoded.append(basetwo(self.bitlist[i]))
            elif t == str:
                string = ""
                for j in range(int(len(self.bitlist[i])/8)):
                    string = "".join([string, chr(basetwo(self.bitlist[i][j*8:(j+1)*8]))])
                decoded.append(string)
        return decoded

    def bitstring(self):
        tmp = deque()
        for i, x in enumerate(self.bitlist):
            if self.types[i] == int and len(x) < 8:
                tmpX = deque(x)
                while len(tmpX) < 8:
                    tmpX.appendleft('0')

                tmp.append("".join(tmpX))
            else:
                tmp.append(x)
        return "".join(tmp)

    def __len__(self):
        return len(self.bitlist)

class GeneticAlgorithm():

    def __init__(self, goal = None, popsize = 25, mutrate = 0.005, 
            crossrate = 75, fitnessFunc = None, maxFitness = None, 
            elitism = True):
        if fitnessFunc == None:
            raise GAException("Need a fitnessfunction to operate!")

        self.goal = goal
        self.popsize = popsize
        self.mutrate = mutrate
        self.crossrate = crossrate
        self.fitnessFunc = fitnessFunc
        self.elitism = elitism


        #if isinstance(maxFitness, function()):
        # elif maxFitness != None:
        #     self.maxFitness = maxFitness
        # else:
        #    raise GAException("Need a specified maxFitnessvalue or a function pointer!")
        self.maxFitness = maxFitness(self)
        self._initPopulation()

    def _initPopulation(self):
        """creates the initial random population"""
        population = []

        for i in range(self.popsize):           
            bitstring = random.getrandbits(len(self.goal.bitstring()))

            bitstring = deque(str(bin(bitstring))[2:])
            while len(bitstring) < len(self.goal.bitstring()):
                bitstring.appendleft('0')

            bitstring = "".join(bitstring)
            population.append(self.createChromosome(self.goal, bitstring))

        self.population = population

    def createChromosome(self, parent, bitstring):
        args = []
        counter = 0
        totalbits = []
        for i, bits in enumerate(parent.bitlist):
            if parent.types[i] == int:
                totalbits.append(8)
            elif parent.types[i] == str:
                totalbits.append(len(bits))

        for i, bits in enumerate(totalbits):
            bitslice = bitstring[counter:counter+bits]
            args.append(self.decode(bitslice, parent.types[i]))
            counter += bits

        return Chromosome(args)

    def decode(self, bitstring, type):
        decoded = None
        if type == int:
            decoded = basetwo(bitstring)
        elif type == str:
            string = ""
            for i in range(int(len(bitstring)/8)):
                string = "".join([string, chr(basetwo(bitstring[i*8:(i+1)*8]))])
            decoded = string
        return decoded

    def rouletteSelection(self):
        roulette = []
        fitsum = sum(x.fitness for x in self.population)
        for i, ch in enumerate(self.population):
            score = max(round(100*ch.fitness*fitsum/self.maxFitness), 1)
            roulette += [i]*score

        a = self.population[random.choice(roulette)]
        b = a
        while b == a:
            b = self.population[random.choice(roulette)]

        return (a, b)

    def evolve(self, elitism = True):
        a, b = self.rouletteSelection()

        newPop = []
        for i in range(int(self.popsize/2)):
            newPop += self.crossover(self.mutate(a), self.mutate(b))
        
        if elitism:
            for i in range(2):
                worst = newPop[0]
                for i, x in enumerate(newPop):
                    if x.fitness < worst.fitness:
                        worst = x

                best = self.population[0]
                for i, x in enumerate(self.population):
                    if x.fitness > best.fitness:
                        best = x

                self.population.remove(best)
                newPop.remove(worst)
                newPop.append(best)                

        self.population = newPop

    def crossover(self, a, b):
        """mate the two chromosomes and return two children"""
        if random.random() < self.crossrate:
            rand = random.random()

            ab = deque(a.bitstring())
            bb = deque(b.bitstring())

            crosspoint = round(len(max(ab,bb))*(rand))

            ab = "".join(ab)
            bb = "".join(bb)

            achild = self.createChromosome(a, ab[:crosspoint]+bb[crosspoint:])
            bchild = self.createChromosome(b, bb[:crosspoint]+ab[crosspoint:])
        else:
            achild, bchild = a, b

        return achild, bchild

    def mutate(self, chromosome):
        """flip a random bit in the chromosome"""
        mut = deque(chromosome.bitstring())

        for i, x in enumerate(mut):
            if random.random() < self.mutrate:
                mut[i] = '0' if mut[i] == '1' else '1'

        mut = "".join(mut)

        return self.createChromosome(chromosome, mut)

    def run(self):
        """let mother nature have its way"""
        res = []
        for r in range(1000):
            self.fitnessFunc(self)            
            res.append([x.decode() for x in self.population])

            purities = [x.fitness for x in self.population]

            #print(max(purities))
            if 1.0 in purities:
                index = purities.index(1.0)
                print("finished on generation:", r)
                print("current generation: ", [x.decode() for x in self.population])
                return res

            self.evolve(self.elitism)

        print("no result...")
        return res