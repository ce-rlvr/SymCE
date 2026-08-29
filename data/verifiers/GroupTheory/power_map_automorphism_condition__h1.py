import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, k = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(k, int)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
            n = len(elements)
            
            image = set()
            for x in elements:
                image.add(x**k)
            is_bijection = (len(image) == n)
            
            is_homomorphism = True
            if is_bijection:
                for x in elements:
                    for y in elements:
                        if ((x*y)**k) != (x**k) * (y**k):
                            is_homomorphism = False
                            break
                    if not is_homomorphism:
                        break
                        
            is_automorphism = is_bijection and is_homomorphism
            gcd_condition = (math.gcd(k, n) == 1)
            
            neg_q = bool(is_automorphism != gcd_condition)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and k is an integer",
    "¬Q: f(x) = x^k is an automorphism iff gcd(k, |G|) = 1 is FALSE"
]
N_HYP = 1
NEG_Q_INDEX = 1