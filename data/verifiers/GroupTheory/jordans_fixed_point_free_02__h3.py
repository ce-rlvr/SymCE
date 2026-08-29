import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: G acts transitively on X",
    "¬Q: Every element in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a finite set
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: G acts transitively on X
    try:
        h3 = bool(witness.is_transitive)
    except Exception:
        h3 = False

    # ¬Q: Every element in G has at least one fixed point in X
    try:
        deg = witness.degree
        if deg == 0:
            # If X is empty, "for all x in X, g.x != x" is vacuously true for any g.
            # Thus there exists g such that for all x, g.x != x.
            # So Q is True, meaning ¬Q is False.
            neg_q = False
        else:
            neg_q = True
            count = 0
            for g in witness.generate():
                count += 1
                if count > 10000:
                    # Safeguard against extremely large groups timing out.
                    # A valid counterexample to this specific conjecture has degree 1.
                    neg_q = False
                    break
                
                has_fixed = False
                for i in range(deg):
                    if g(i) == i:
                        has_fixed = True
                        break
                
                if not has_fixed:
                    # Found a derangement (an element with no fixed points)
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]