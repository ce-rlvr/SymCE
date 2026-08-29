import sympy
import sympy.combinatorics as combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = combinatorics.PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
    
    # H1: G is a nilpotent group
    try:
        val = G.is_nilpotent
        h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a central series of G that includes N as one of its terms.
    try:
        if not isinstance(N, combinatorics.PermutationGroup):
            is_sub = False
            is_norm = False
        else:
            is_sub = True
            for gen in N.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            
            is_norm = True
            if is_sub:
                for g in G.generators:
                    for n in N.generators:
                        conj = g**-1 * n * g
                        if not N.contains(conj):
                            is_norm = False
                            break
                    if not is_norm:
                        break
            else:
                is_norm = False
                
        val = G.is_nilpotent
        g_nilp = bool(val() if callable(val) else val)
        
        # A central series of G containing N exists iff G is nilpotent and N is a normal subgroup of G.
        q = g_nilp and is_sub and is_norm
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: There does not exist a central series of G that includes N as one of its terms"
]

N_HYP = 1
NEG_Q_INDEX = 1