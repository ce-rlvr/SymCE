import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import isprime

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    G = None
    p, q, r = 2, 3, 5
    
    try:
        if isinstance(witness, dict):
            G = witness.get('G', None)
            p = witness.get('p', 2)
            q = witness.get('q', 3)
            r = witness.get('r', 5)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, p, q, r = witness
            elif len(witness) >= 1:
                G = witness[0]
        else:
            G = witness
    except Exception:
        pass

    # H_1: G is a finite group
    h1 = False
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
    except Exception:
        pass

    # H_2: p, q, and r are distinct prime numbers
    h2 = False
    try:
        if isprime(p) and isprime(q) and isprime(r) and len({p, q, r}) == 3:
            h2 = True
    except Exception:
        pass

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    neg_q = False
    try:
        if hasattr(G, 'is_simple'):
            if callable(G.is_simple):
                neg_q = bool(G.is_simple())
            else:
                neg_q = bool(G.is_simple)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p, q, and r are distinct prime numbers",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2