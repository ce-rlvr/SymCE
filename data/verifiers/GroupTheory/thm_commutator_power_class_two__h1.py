import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        if isinstance(witness, dict):
            G = witness['G']
            n = witness['n']
            x = witness['x']
            y = witness['y']
        else:
            G, n, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        D = G.derived_subgroup()
        Z = G.center()
        h1 = bool(D.is_subgroup(Z))
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int)
    except Exception:
        h2 = False
        
    try:
        h3 = bool((x in G) and (y in G))
    except Exception:
        h3 = False
        
    try:
        def comm(a, b):
            return (~a) * (~b) * a * b
            
        lhs = comm(x**n, y)
        rhs = comm(x, y)**n
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: commutator subgroup is contained in Z(G)", "H_2: n is an integer", "H_3: x and y are elements of G", "not Q: comm(x**n, y) != comm(x, y)**n"]

N_HYP = 3
NEG_Q_INDEX = 3