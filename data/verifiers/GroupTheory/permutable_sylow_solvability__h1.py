import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False]
            
        order = witness.order()
        primes = list(factorint(order).keys())
        
        h1_ok = True
        for i in range(len(primes)):
            for j in range(i + 1, len(primes)):
                p = primes[i]
                q = primes[j]
                
                try:
                    P0 = witness.sylow_subgroup(p)
                    Q0 = witness.sylow_subgroup(q)
                except Exception:
                    h1_ok = False
                    break
                
                target_order = P0.order() * Q0.order()
                
                found = False
                # Iterate over all elements to find a conjugate of Q0 that permutes with P0.
                # PQ = QP is equivalent to <P, Q> having order |P| * |Q|.
                for g in witness.elements:
                    Q_g_gens = [g * gen * (~g) for gen in Q0.generators]
                    gens = P0.generators + Q_g_gens
                    if not gens:
                        H = PermutationGroup(Permutation())
                    else:
                        H = PermutationGroup(*gens)
                        
                    if H.order() == target_order:
                        found = True
                        break
                
                if not found:
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    try:
        neg_q = not witness.is_solvable
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: For every pair of primes p and q dividing the order of G, G contains a Sylow p-subgroup P and a Sylow q-subgroup Q such that PQ = QP",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1