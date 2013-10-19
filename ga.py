import random


class GAException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Gene():

    def __init__(self, *phenotype):
        self.phenotype = phenotype

    def encode(self):
        """Encode the genes to a bitstring"""
        enc = ""
        for genome in self.phenotype:
            if isinstance(genome, str):
                for c in genome:
                    enc = "".join([enc, bin(ord(c))])
            elif isinstance(genome, (int, hex)):
                enc = "".join([enc, bin(genome)])
        return enc[2:]


class Chromosome():

    def __init__(self, *genotype):
        self.genotype = genotype
        self.fitness = 0

    def encode(self):
        """Encode the set of genes to a bitstring"""
        enc = ""
        for genome in self.genotype:
            enc = "".join([enc, genome.encode()])
        return enc

    def __str__(self):
        return repr(self.encode())


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
            bitstring = random.getrandbits(len(self.goal.encode()))
            tmpChr = Chromosome(Gene(bitstring))
            population.append(tmpChr)
    
        self.population = population

    def decode(self, bitstring):
        pass

    def encode(self, chromosome):
        pass

    def evolve(self, procreations):
        for i in range(procreations):
            # Change to make better choices (higher fitness = higher chance to be picked)
            roulette = []
            fitSum = sum([x.fitness for x in self.population])
            for i, ch in enumerate(self.population):
                roulette += [i]*round(100*ch.fitness/fitSum)

            index = roulette[random.randint(0, len(roulette)-1)]
            a = self.population[index]
            while index in roulette:
                roulette.remove(index)

            index = roulette[random.randint(0, len(roulette)-1)]
            b = self.population[index]
            #a, b = random.sample(self.population, 2)
            ai = self.population.index(a)
            bi = self.population.index(b)

            if random.randint(0,100) < self.crossrate: 
                a, b = self.crossover(a, b)

            a = self.mutate(a)
            b = self.mutate(b)

            self.population[ai] = a
            self.population[bi] = b

    def crossover(self, a, b):
        """mate the two chromosomes and return two children"""
        rand = random.randint(1, 99)
        crosspoint = round(len(self.goal.encode())*(rand/100))

        a = a.encode()
        b = b.encode()

        # Prevent the chromosomes from shrinking
        goal = self.goal.encode()
        a = list(a)
        b = list(b)
        while len(a) < len(goal):
            a = ['0'] + a
        while len(b) < len(goal):
            b = ['0'] + b

        a = "".join(a)
        b = "".join(b)

        achild = Chromosome(Gene(int(a[:crosspoint]+b[crosspoint:], 2)))
        bchild = Chromosome(Gene(int(b[:crosspoint]+a[crosspoint:], 2)))

        return (achild, bchild)

    def mutate(self, chromosome):
        """flip a random bit in the chromosome"""
        mut = list(chromosome.encode())
        while len(mut) < len(self.goal.encode()):
            mut = ['0'] + mut

        for i in range(len(mut)):
            if random.randint(0,100) < self.mutrate:
                mut[i] = '0' if i == '1' else '1'

        mut = "".join(mut)
        return Chromosome(Gene(int(mut, 2)))

    def fit(self):
        """adjust the fitness of each chromosome"""
        for ch in self.population:
            goal = int(self.goal.encode(), 2)
            chSc = int(ch.encode(), 2)
            ch.fitness = goal/(chSc if chSc != 0 else 1)

    def run(self):
        """let mother nature have its way"""
        for r in range(1000):
            self.fit()
            purities = [x.fitness for x in self.population]            
            if 1.0 in purities:
                index = purities.index(1.0)
                print("finished on generation:", r)
                print("current generation: ", [x.encode() for x in self.population])
                return self.population[index]

            self.evolve(1)

        print([x.encode() for x in self.population])
        return "no result..."