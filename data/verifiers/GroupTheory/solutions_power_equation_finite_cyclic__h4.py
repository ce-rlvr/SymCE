import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
    # Extract G and m from the witness
    G = None
    m = None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, m = witness
    else:
        G = witness
        m = getattr(G, 'm', 2) # Fallback if m is provided as an attribute

    # H_1: Let G be a cyclic group.
    try:
        is_cyclic = getattr(G, 'is_cyclic')
        if callable(is_cyclic):
            h1 = bool(is_cyclic())
        else:
            h1 = bool(is_cyclic)
    except Exception:
        h1 = False

    # H_2: Let the order of G be a finite integer n.
    try:
        n_attr = getattr(G, 'order')
        if callable(n_attr):
            n = n_attr()
        else:
            n = n_attr
        h2 = (isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer)) and n > 0
    except Exception:
        h2 = False

    # H_3: Let e be the identity element of G.
    try:
        e_attr = getattr(G, 'identity')
        if callable(e_attr):
            e = e_attr()
        else:
            e = e_attr
        h3 = e is not None
    except Exception:
        h3 = False

    # ¬Q: The number of elements x in G satisfying x^m = e is NOT exactly gcd(m,n).
    try:
        elements = getattr(G, 'elements')
        if callable(elements):
            elements = elements()
            
        count = 0
        for x in elements:
            if x**m == e:
                count += 1
                
        expected = math.gcd(abs(int(m)), int(n))
        neg_q = count != expected
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: The order of G is a finite integer n",
    "H_3: e is the identity element of G",
    "¬Q: The number of elements x in G satisfying x^m = e is NOT exactly gcd(m,n)"
]

N_HYP = 3
NEG_Q_INDEX = 3