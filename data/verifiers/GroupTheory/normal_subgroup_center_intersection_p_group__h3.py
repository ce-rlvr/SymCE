import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    p = None
    G = None
    N = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, G, N = witness
            elif len(witness) == 2:
                G, N = witness
                try:
                    factors = sympy.ntheory.factorint(G.order())
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                except Exception:
                    pass
        elif isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
            N = witness.get('N')
            if p is None and G is not None:
                try:
                    factors = sympy.ntheory.factorint(G.order())
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                except Exception:
                    pass
    except Exception:
        pass

    try:
        p = int(p)
    except Exception:
        pass

    # H1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False

    # H2: G is a finite group of order p^n for some integer n >= 1
    try:
        order = G.order()
        factors = sympy.ntheory.factorint(order)
        h2 = (len(factors) == 1) and (p in factors) and (factors[p] >= 1)
    except Exception:
        h2 = False

    # neg_Q: The intersection N \cap Z(G) does NOT contain more than just the identity element
    try:
        if hasattr(N, 'elements'):
            n_elems = list(N.elements)
        else:
            n_elems = list(N)
            
        center = G.center()
        center_elems = list(center.elements)
        
        intersection = [g for g in n_elems if g in center_elems]
        
        has_non_identity = False
        for g in intersection:
            if hasattr(G, 'identity') and g == G.identity:
                continue
            if hasattr(g, 'is_Identity') and g.is_Identity:
                continue
            has_non_identity = True
            break
            
        neg_q = not has_non_identity
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite group of order p^n for some integer n >= 1",
    "¬Q: The intersection N \\cap Z(G) contains only the identity element"
]

N_HYP = 2
NEG_Q_INDEX = 2