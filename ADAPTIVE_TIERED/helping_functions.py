__author__ = 'erisa'
MAX_NUM_NODE = 50000000
import random as rnd
def fast_randint(n):
    '''Return an integer uniformly at random between 0 and n-1, inclusive.
    The code is based on an excerpt from random.py and is probably faster than random.randint().'''
    k = int(n).bit_length()
    r = rnd.getrandbits(k)
    while r >= n:
        r = rnd.getrandbits(k)
    return r
def hash_function(a,b):
    if a > b:
        a, b = b, a
    return a + b * MAX_NUM_NODE
def check_condition(M, t, alpha, triangles):
    one_res = (1.0*M/t)**5
    if triangles == 0:
        return 1
    two_res = ((M - alpha * M)/t)**4 * ((alpha * M)/triangles)**2
    # print t,M, alpha, triangles, one_res,two_res
    if one_res > two_res:
        return 1
    else:
        return 2

