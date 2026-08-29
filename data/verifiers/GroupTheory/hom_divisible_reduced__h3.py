import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
        D, R, f = witness
    except Exception:
        return [False, False, False]

    # H1: D is a divisible abelian group
    try:
        if not D.is_abelian:
            h1 = False
        else:
            elements_D = list(D.elements)
            if len(elements_D) > 100:
                h1 = False
            else:
                h1 = True
                # A finite group is divisible iff it is the trivial group.
                # We verify this by checking if the equation x**n == g has a solution
                # for all g in D and all n up to |D| + 1.
                for n in range(1, len(elements_D) + 2):
                    for g in elements_D:
                        if not any(x**n == g for x in elements_D):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H2: R is a reduced abelian group
    try:
        if not R.is_abelian:
            h2 = False
        else:
            elements_R = list(R.elements)
            if len(elements_R) > 100:
                h2 = False
            else:
                # Any finite abelian group is reduced because its only 
                # divisible subgroup is the trivial group.
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: f is NOT the trivial homomorphism
    try:
        elements_D = list(D.elements)
        elements_R = list(R.elements)
        id_R = R.identity
        
        if isinstance(f, list):
            f = dict(f)
            
        is_trivial = True
        is_valid_map = True
        for d in elements_D:
            if isinstance(f, dict):
                if d not in f:
                    is_valid_map = False
                    break
                val = f[d]
            else:
                val = f(d)
                
            if val not in elements_R:
                is_valid_map = False
                break
                
            if val != id_R:
                is_trivial = False
                
        if not is_valid_map:
            neg_q = False
        else:
            neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: D is a divisible abelian group",
    "H_2: R is a reduced abelian group",
    "¬Q: f is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2