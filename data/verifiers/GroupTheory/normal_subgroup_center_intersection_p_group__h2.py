import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    try:
        if len(witness) == 3:
            p, G, N = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: N is a non-trivial normal subgroup of G
    try:
        h2_ok = False
        n_elements = list(N.elements)
        if len(n_elements) > 1:
            # Check if N is a subgroup of G
            is_sub = True
            for gen in N.generators:
                if gen not in G:
                    is_sub = False
                    break
            
            if is_sub:
                # Check normality: g * n * g^-1 in N for all g in G, n in N
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * (~g)) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                if is_norm:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: N \cap Z(G) contains ONLY the identity element
    try:
        # Find the center Z(G)
        Z_elements = set()
        for g in G.elements:
            commutes = True
            for gen in G.generators:
                if g * gen != gen * g:
                    commutes = False
                    break
            if commutes:
                Z_elements.add(g)
                
        # Find intersection size of N and Z(G)
        intersection_size = 0
        for n in N.elements:
            if n in Z_elements:
                intersection_size += 1
                
        neg_q_ok = (intersection_size == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a non-trivial normal subgroup of G",
    "¬Q: N intersect Z(G) contains only the identity element"
]

N_HYP = 2
NEG_Q_INDEX = 2