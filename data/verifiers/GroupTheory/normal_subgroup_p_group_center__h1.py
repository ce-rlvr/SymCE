import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        else:
            G, N = witness
    except Exception:
        return [False, False, False]

    # H1: N is a normal subgroup of G
    try:
        h1_ok = True
        # Check if N is a subgroup of G
        for n in N.generators:
            if n not in G:
                h1_ok = False
                break
        if h1_ok:
            # Check normality: g * n * g^-1 in N for all generators
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1_ok = False
                        break
                    if (~g * n * g) not in N:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: N is not the trivial subgroup
    try:
        h2_ok = bool(N.order() > 1)
    except Exception:
        h2_ok = False

    # neg_Q: The intersection of N and Z(G) is trivial
    try:
        neg_q_ok = True
        for n in N.elements:
            # Skip the identity element
            if getattr(n, 'is_Identity', False) or n == n**0:
                continue
            
            # Check if n is in the center of G, Z(G)
            in_center = True
            for g in G.generators:
                if n * g != g * n:
                    in_center = False
                    break
            
            if in_center:
                # Found a non-identity element in N intersect Z(G)
                neg_q_ok = False
                break
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is not the trivial subgroup",
    "¬Q: The intersection of N and Z(G) is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2