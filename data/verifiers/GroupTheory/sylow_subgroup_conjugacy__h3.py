import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
        # The witness is expected to be a tuple: (G, p, P, Q)
        if len(witness) != 4:
            return [False, False, False]
        G, p, P, Q = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # ¬Q: There is NO element g in G such that gPg^{-1} = Q
    try:
        if not h1:
            neg_q = False
        else:
            G_elems = set(G.elements)
            
            # Handle the case where P and Q are single elements
            if isinstance(P, Permutation) and isinstance(Q, Permutation):
                exists_g = False
                for g in G_elems:
                    if g * P * ~g == Q:
                        exists_g = True
                        break
                neg_q = not exists_g
            else:
                # Handle the case where P and Q are subgroups or subsets
                def get_elems(X):
                    if hasattr(X, 'elements'):
                        return set(X.elements)
                    return set(X)
                
                P_elems = get_elems(P)
                Q_elems = get_elems(Q)
                
                exists_g = False
                for g in G_elems:
                    conj_P = set(g * x * ~g for x in P_elems)
                    if conj_P == Q_elems:
                        exists_g = True
                        break
                neg_q = not exists_g
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: There is no element g in G such that gPg^{-1} = Q"
]

N_HYP = 2
NEG_Q_INDEX = 2