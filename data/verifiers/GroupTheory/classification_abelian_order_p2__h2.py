import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy import eye, zeros, MatrixBase
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_2: The order of G is p^2",
    "¬Q: G is not isomorphic to either Z/p^2Z or (Z/pZ) x (Z/pZ)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            if hasattr(G, 'order'):
                order = G.order()
            elif hasattr(G, 'is_Matrix') and G.is_Matrix:
                order = G.rows
            else:
                order = len(G)
            p = int(math.isqrt(order))
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: The order of G is p^2
    try:
        if hasattr(G, 'order'):
            order = G.order()
        elif hasattr(G, 'is_Matrix') and G.is_Matrix:
            order = G.rows
        else:
            order = len(G)
        h2 = bool(order == p**2)
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to either Z/p^2Z or (Z/pZ) x (Z/pZ)
    # Since all valid groups of order p^2 are isomorphic to one of these,
    # the conclusion fails (¬Q is True) iff G is NOT a valid group.
    try:
        is_iso = False
        
        if isinstance(G, (PermutationGroup, FpGroup)):
            is_iso = True
        elif hasattr(G, 'is_Matrix') and G.is_Matrix:
            n = G.rows
            if G.cols == n:
                is_valid = True
                elements = set(G)
                if elements != set(range(n)):
                    is_valid = False
                else:
                    for i in range(n):
                        if len(set(G[i, :])) != n: is_valid = False
                        if len(set(G[:, i])) != n: is_valid = False
                    if is_valid:
                        for i in range(n):
                            for j in range(n):
                                for k in range(n):
                                    if G[G[i, j], k] != G[i, G[j, k]]:
                                        is_valid = False
                is_iso = is_valid
        elif isinstance(G, (list, set, tuple)):
            G_list = list(G)
            if G_list:
                # Check if it forms a group under multiplication
                try:
                    has_id = False
                    for e in G_list:
                        if all(e * a == a and a * e == a for a in G_list):
                            has_id = True
                            break
                    if has_id:
                        closed = True
                        for a in G_list:
                            for b in G_list:
                                if (a * b) not in G_list:
                                    closed = False
                                    break
                            if not closed: break
                        if closed:
                            is_iso = True
                except Exception:
                    pass
                
                # Check if it forms a group under addition
                if not is_iso:
                    try:
                        has_id = False
                        for e in G_list:
                            if all(e + a == a and a + e == a for a in G_list):
                                has_id = True
                                break
                        if has_id:
                            closed = True
                            for a in G_list:
                                for b in G_list:
                                    if (a + b) not in G_list:
                                        closed = False
                                        break
                                if not closed: break
                            if closed:
                                is_iso = True
                    except Exception:
                        pass
        
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]