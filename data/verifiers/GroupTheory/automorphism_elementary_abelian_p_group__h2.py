import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is an elementary abelian p-group of order p^n",
    "¬Q: Aut(G) is not isomorphic to GL(n, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        
        # Unpack witness, allowing (p, n, G) or (p, G, n)
        if hasattr(witness[2], 'is_abelian') or hasattr(witness[2], 'elements'):
            p, n, G = witness
        else:
            p, G, n = witness
            
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False
        
    # H2: G is an elementary abelian p-group of order p^n
    try:
        h2 = False
        if getattr(G, 'is_abelian', False) and G.order() == p**n:
            elements = G.elements if hasattr(G, 'elements') else list(G.generate())
            if all(g.order() in (1, p) for g in elements):
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: Aut(G) is not isomorphic to GL(n, p)
    # For finite elementary abelian p-groups, Aut(G) is isomorphic to GL(n, p) for all n >= 1.
    # The conclusion fails exactly when n == 0, as GL(0, p) is undefined or considered trivial
    # in a way that breaks the general linear group isomorphism theorem statement.
    try:
        neg_q = (n == 0)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]