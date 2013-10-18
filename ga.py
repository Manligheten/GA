class GAException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Gene():

    def __init__(self, *phenotype):
        # phenotype = (trait, value)
        if len(phenotype[0]) == 2:
            self.phenotype = phenotype[0]
        else:
            raise GAException("".join(["Phenotype has to be of length 2,", 
                str(len(phenotype)), " given"]))


class Chromosome():

    def __init__(self, genes):
        self.genotype = genes

#phenotype

def recombine(a, b):
    pass

def mutate(gene):
    pass