import random
from math import floor

class GAException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# class Gene():

#     def __init__(self, *phenotype):
#         self.phenotype = phenotype

#     def encode(self):
#         """Encode the genes to a bitstring"""
#         enc = ""
#         for genome in self.phenotype:
#             if isinstance(genome, str):
#                 for c in genome:
#                     enc = "".join([enc, bin(ord(c))])
#             elif isinstance(genome, (int, hex)):
#                 enc = "".join([enc, bin(genome)])
#         return enc[2:]


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
                    tmp = bin(ord(c))[2:]
                    while len(tmp) < 8:
                        tmp = "".join(['0', tmp])                    
                    enc = "".join([enc, tmp])                
            
            self.bitlist.append(enc)
            self.types.append(type(gene))

    def decode(self):
        decoded = []
        for i, t in enumerate(self.types):
            if t == int:
                decoded.append(t(self.bitlist[i], 2))
            elif t == str:
                string = ""
                for j in range(int(len(self.bitlist[i])/8)):
                    string = "".join([string, chr(int(self.bitlist[i][j*8:(j+1)*8], 2))])
                decoded.append(string)
        return decoded

    def bitstring(self):
        return "".join(self.bitlist)

    def __len__(self):
        return len(self.bitlist)

class GeneticAlgorithm():

    def __init__(self, goal, popSize, mutrate = 10, crossrate = 70):
        self.goal = goal
        self.popSize = popSize
        self.mutrate = mutrate
        self.crossrate = crossrate

        self._initPopulation()

    def _initPopulation(self):
        """creates the initial random population"""
        population = []

        for i in range(self.popSize):           
            bitstring = random.getrandbits(len(self.goal.bitstring()))

            bitstring = list(str(bin(bitstring))[2:])
            while len(bitstring) < len(self.goal.bitstring()):
                bitstring = ['0'] + bitstring

            bitstring = "".join(bitstring)
            population.append(self.createChromosome(self.goal, bitstring))

        self.population = population

    def createChromosome(self, parent, bitstring):
        args = []
        counter = 0
        for i, bits in enumerate(parent.bitlist):
            bitslice = bitstring[counter:counter+len(bits)]
            args.append(self.decode(bitslice, parent.types[i]))
            counter = len(bits)

        return Chromosome(args)

    def decode(self, bitstring, type):
        decoded = None
        if type == int:
            decoded = int(bitstring, 2)
        elif type == str:
            string = ""
            for j in range(int(len(bitstring)/8)):
                string = "".join([string, chr(int(bitstring[j*8:(j+1)*8], 2))])
            decoded = string
        return decoded

    def rouletteSelection(self):
        roulette = []
        fitSum = sum([x.fitness for x in self.population])
        for i, ch in enumerate(self.population):
            roulette += [i]*((floor(100*ch.fitness/fitSum if fitSum != 0 else 1)+1))

        a = self.population[random.choice(roulette)]
        b = a
        while b == a:
            b = self.population[random.choice(roulette)]

        #print(a.decode(), b.decode())
        return (a, b)

    def evolve(self):
        a, b = self.rouletteSelection()

        newPop = []
        for i in range(int(self.popSize/2)):
            newPop += self.crossover(self.mutate(a), self.mutate(b))
            

        self.population = newPop

    def crossover(self, a, b):
        """mate the two chromosomes and return two children"""
        if random.random() < self.crossrate:
            rand = random.random()
            goal = self.goal.bitstring()

            ab = a.bitstring()
            bb = b.bitstring()

            crosspoint = round(len(max(ab,bb))*(rand))
            
            # Prevent the chromosomes from shrinking
            while len(ab) < len(bb):
                ab = "".join(['0', ab])
            while len(bb) < len(ab):
                bb = "".join(['0', bb])

            achild = self.createChromosome(a, ab[:crosspoint]+bb[crosspoint:])
            bchild = self.createChromosome(b, bb[:crosspoint]+ab[crosspoint:])
        else:
            achild, bchild = a, b

        return achild, bchild

    def mutate(self, chromosome):
        """flip a random bit in the chromosome"""
        mut = list(chromosome.bitstring())
        while len(mut) < len(self.goal.bitstring()):
            mut = ['0'] + mut

        for i in range(len(mut)):
            if random.random() < self.mutrate:
                mut[i] = '0' if mut[i] == '1' else '1'

        mut = "".join(mut)

        return self.createChromosome(chromosome, mut)

    # def fit(self):
    #     """adjust the fitness of each chromosome"""
    #     for ch in self.population:
    #         goal = int(self.goal.bitstring(), 2)
    #         chSc = int(ch.bitstring(), 2)
    #         ch.fitness = round(goal/(chSc if chSc != 0 else 1), 2)

    def fit(self):
        """adjust the fitness of each chromosome"""
        goal = self.goal.bitstring()
        step = 1/len(goal)
        for ch in self.population:
            bitstring = ch.bitstring()

            fitness = 0.0
            while len(bitstring) < len(goal):
                bitstring = "".join(['0', bitstring])

            for i in range(len(bitstring)):
                if bitstring[i] == goal[i]:
                    fitness += step

            ch.fitness = fitness

    def run(self):
        """let mother nature have its way"""
        res = []
        for r in range(100):
            self.fit()            
            res.append([x.decode() for x in self.population])

            purities = [x.fitness for x in self.population]
            if 1.0 in purities:
                index = purities.index(1.0)
                print("finished on generation:", r)
                print("current generation: ", [x.decode() for x in self.population])
                return res

            self.evolve()

        print("no result...")
        return res