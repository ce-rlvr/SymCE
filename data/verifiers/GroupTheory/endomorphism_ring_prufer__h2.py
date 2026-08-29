import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            if sympy.isprime(witness[0]) and not sympy.isprime(witness[1]):
                p, G = witness
            else:
                G, p = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    # neg_Q: The endomorphism ring of G is not isomorphic to Z_p
    try:
        # Z_p is infinite. If G is a finite group, its endomorphism ring is finite.
        # Thus, they cannot be isomorphic.
        is_fin = False
        if isinstance(G, PermutationGroup):
            is_fin = True
        elif hasattr(G, 'order'):
            if G.order() < float('inf'):
                is_fin = True
        elif hasattr(G, 'is_finite') and G.is_finite:
            is_fin = True
            
        if is_fin:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The endomorphism ring of G is not isomorphic to the ring of p-adic integers Z_p"
]

N_HYP = 1
NEG_Q_INDEX = 1