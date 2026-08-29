import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]

    # H1: N and H are groups
    try:
        h1 = (hasattr(N, 'elements') and hasattr(H, 'elements') and 
              hasattr(N, 'identity') and hasattr(H, 'identity'))
    except Exception:
        h1 = False

    # H2: G = N \rtimes_\phi H is the external semidirect product
    # We verify that phi is a valid map H x N -> N
    try:
        h2 = callable(phi)
        if h2:
            for h in H.elements:
                for n in N.elements:
                    if phi(h, n) not in N.elements:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails at the witness
    try:
        # Compute LHS: Z(G) \cap (N \times {1_H})
        # An element (n, 1_H) is in Z(G) iff for all (m, k) in G:
        # (n, 1_H)(m, k) == (m, k)(n, 1_H)
        # n * phi_{1_H}(m) == m * phi_k(n)
        lhs = set()
        id_H = H.identity
        for n in N.elements:
            is_in_Z = True
            for m in N.elements:
                for k in H.elements:
                    left = n * phi(id_H, m)
                    right = m * phi(k, n)
                    if left != right:
                        is_in_Z = False
                        break
                if not is_in_Z:
                    break
            if is_in_Z:
                lhs.add(n)

        # Compute RHS: { n \in Z(N) | phi_h(n) = n for all h \in H }
        rhs = set()
        for n in N.elements:
            in_ZN = True
            for m in N.elements:
                if n * m != m * n:
                    in_ZN = False
                    break
            if not in_ZN:
                continue

            fixed = True
            for h in H.elements:
                if phi(h, n) != n:
                    fixed = False
                    break
            if fixed:
                rhs.add(n)

        neg_Q = (lhs != rhs)
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product",
    "¬Q: The intersection Z(G) \\cap (N \\times {1_H}) is NOT equal to the specified set"
]

N_HYP = 2
NEG_Q_INDEX = 2