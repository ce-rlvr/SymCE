import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, G = witness
                X = G.free_group.generators
            elif len(witness) == 3:
                n, X, R = witness
                if len(R) > 0:
                    F = R[0].group
                elif len(X) > 0 and hasattr(X[0], 'group'):
                    F = X[0].group
                else:
                    F, _ = free_group(','.join(str(x) for x in X))
                G = FpGroup(F, R)
            else:
                return [False, False, False]
        elif hasattr(witness, 'free_group'):
            G = witness
            n = len(G.free_group.generators)
            X = G.free_group.generators
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let n be a positive integer.
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: Let X = {x_1, x_2, ..., x_n} be a set of n distinct generators.
    try:
        h2 = len(X) == n and len(set(X)) == n
    except Exception:
        h2 = False

    # ¬Q: The group defined by the presentation <X | R> is NOT isomorphic to the free abelian group of rank n.
    try:
        # A finitely generated group is isomorphic to the free abelian group of rank n
        # if and only if it is abelian and its abelian invariants are exactly [0]*n.
        invs = G.abelian_invariants()
        is_iso = True
        
        if sorted(invs) != [0] * n:
            is_iso = False
        else:
            # Check if G is abelian by verifying all generator commutators are trivial
            gens = G.generators
            for i in range(len(gens)):
                for j in range(i + 1, len(gens)):
                    g1 = gens[i]
                    g2 = gens[j]
                    comm = g1 * g2 * g1**-1 * g2**-1
                    if comm != G.identity:
                        is_iso = False
                        break
                if not is_iso:
                    break
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: X is a set of n distinct generators",
    "¬Q: The group defined by the presentation <X | R> is not isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2