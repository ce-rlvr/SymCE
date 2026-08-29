import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness):
    try:
        G, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = hasattr(G, 'sylow_subgroup') and bool(G.is_abelian)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h2 = False
        
    try:
        P = G.sylow_subgroup(p)
        is_normal = True
        for g in G.generators:
            for h in P.generators:
                if not P.contains(g * h * ~g):
                    is_normal = False
                    break
            if not is_normal:
                break
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: p is a prime number",
    "¬Q: G does not have exactly one Sylow p-subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2