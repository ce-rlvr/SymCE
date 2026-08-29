import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.matrices import eye, zeros
from itertools import product

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    # Parse witness: can be (G, n) or (G, n, H)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, n = witness
                try:
                    ds = G.derived_series()
                    H = ds[n] if n < len(ds) else ds[-1]
                except Exception:
                    H = None
            elif len(witness) == 3:
                G, n, H = witness
            else:
                G, n, H = None, None, None
        else:
            G, n, H = None, None, None
    except Exception:
        G, n, H = None, None, None

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G^(n) is the n-th derived subgroup of G
    try:
        if h1_ok and isinstance(n, (int, sympy.Integer)) and n >= 0 and isinstance(H, PermutationGroup):
            ds = G.derived_series()
            expected_H = ds[n] if n < len(ds) else ds[-1]
            h2_ok = bool(H.is_subgroup(G) and expected_H.is_subgroup(H) and H.is_subgroup(expected_H))
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: G^(n) is not a fully characteristic subgroup of G
    try:
        if h1_ok and h2_ok:
            is_fully_char = True
            elements = list(G.generate())
            gens = G.generators
            iterations = 0
            for imgs in product(elements, repeat=len(gens)):
                iterations += 1
                if iterations > 5000:
                    break
                try:
                    phi = homomorphism(G, G, gens, imgs)
                except ValueError:
                    continue
                except Exception:
                    continue
                
                for h in H.generators:
                    if phi(h) not in H:
                        is_fully_char = False
                        break
                if not is_fully_char:
                    break
            neg_q_ok = not is_fully_char
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G^(n) is the n-th derived subgroup of G",
    "¬Q: G^(n) is not a fully characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2