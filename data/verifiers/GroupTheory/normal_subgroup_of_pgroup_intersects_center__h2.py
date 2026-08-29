import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

# Group theory named bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Linear algebra named bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, p).
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, N, p = witness
            elif len(witness) == 2:
                G, N = witness
                p = 2  # Default to 2 if omitted
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_subgroup = True
            for n in N.generators:
                if n not in G:
                    is_subgroup = False
                    break
            
            if is_subgroup:
                is_normal = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_normal = False
                            break
                        if (~g * n * g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False

    # H_3: N is not the trivial subgroup
    try:
        h3 = False
        if isinstance(N, PermutationGroup):
            h3 = bool(N.order() > 1)
    except Exception:
        h3 = False

    # ¬Q: The intersection of N and Z(G) is the trivial subgroup
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            Z = G.center()
            intersection_trivial = True
            for z in Z.generate():
                if z.is_Identity:
                    continue
                if z in N:
                    intersection_trivial = False
                    break
            neg_q = intersection_trivial
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a normal subgroup of G",
    "H_3: N is not the trivial subgroup",
    "¬Q: The intersection of N and Z(G) is the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3