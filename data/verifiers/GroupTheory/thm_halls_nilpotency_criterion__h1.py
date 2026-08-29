import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a nilpotent group",
    "H_3: The quotient group G/N' is nilpotent",
    "not Q: The group G is not nilpotent"
]

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(G.is_normal(N))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(N.is_nilpotent)
    except Exception:
        h2 = False
        
    try:
        H = N.derived_subgroup()
        h3_evaluated = False
        
        if hasattr(G, 'quotient_group'):
            try:
                Q = G.quotient_group(H)
                h3 = bool(Q.is_nilpotent)
                h3_evaluated = True
            except Exception:
                pass
                
        if not h3_evaluated:
            try:
                order_G = G.order()
                primes = factorint(order_G).keys()
                h3 = True
                for p in primes:
                    P = G.sylow_subgroup(p)
                    PH_gens = list(P.generators) + list(H.generators)
                    PH = PermutationGroup(PH_gens)
                    if not G.is_normal(PH):
                        h3 = False
                        break
                h3_evaluated = True
            except Exception:
                pass
                
        if not h3_evaluated:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        neg_q = not bool(G.is_nilpotent)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]