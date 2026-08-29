import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
        if isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
            N = witness.get('N')
        else:
            p, G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: G is a finite p-group
    try:
        h2 = False
        if getattr(G, 'is_group', False):
            order = G.order()
            if order == 1:
                h2 = True
            elif h1:
                factors = sympy.factorint(order)
                if list(factors.keys()) == [p]:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: The quotient group G/N is not a p-group
    try:
        neg_q = False
        if not getattr(N, 'is_group', False):
            # N is not a group, so G/N is undefined (not a p-group)
            neg_q = True
        elif not all(g in G for g in N.generators):
            # N is not a subgroup of G
            neg_q = True
        else:
            # Check if N is a normal subgroup of G
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                # If N is not normal, G/N is not a group, hence not a p-group
                neg_q = True
            else:
                # N is normal, so G/N is a valid quotient group
                Q_group = G.quotient_group(N)
                q_order = Q_group.order()
                if q_order == 1:
                    neg_q = False
                else:
                    factors = sympy.factorint(q_order)
                    if list(factors.keys()) != [p]:
                        neg_q = True
    except Exception:
        # Any failure in quotient group computation implies it's not a valid p-group
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "¬Q: The quotient group G/N is not a p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2