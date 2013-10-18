from ga import *


def main():
    a = Gene(("color", 0xffffff))
    b = Gene(("color", 0x000000))
    ch = Chromosome([a, b])
    print(ch.genotype)


if __name__ == '__main__':
    main()