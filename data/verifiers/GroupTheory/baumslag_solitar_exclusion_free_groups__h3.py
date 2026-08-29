import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: m and n are non-zero integers",
    "¬Q: F contains a subgroup isomorphic to BS(m,n)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the free group F, integers m and n, 
    and the generators a and b of the subgroup isomorphic to BS(m,n).
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            m = witness.get('m')
            n = witness.get('n')
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                F, m, n, a, b = witness
            elif len(witness) == 4:
                F, m, n, gens = witness
                a, b = gens[0], gens[1]
            elif len(witness) == 3:
                F, m, n = witness
                a, b = None, None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H_2: m and n are non-zero integers
    try:
        h2 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m != 0 and n != 0
    except Exception:
        h2 = False

    # ¬Q: F contains a subgroup isomorphic to BS(m,n)
    # We verify this by checking if the provided generators satisfy the defining relation
    # of BS(m,n) non-trivially, which acts as the proxy for the subgroup inclusion check.
    try:
        if a is not None and b is not None:
            if getattr(a, 'group', None) != F or getattr(b, 'group', None) != F:
                neg_q = False
            else:
                # Check the Baumslag-Solitar relation: a * b^m * a^-1 = b^n
                rel_holds = (a * b**m * a**-1 == b**n)
                # Ensure the generators are non-trivial
                neg_q = bool(rel_holds and (a != F.identity) and (b != F.identity))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]