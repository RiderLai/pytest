import itertools


def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    gen = itertools.count(first, step)
    if end is not None:
        gen = itertools.takewhile(lambda n: n < end, gen)
    return gen
