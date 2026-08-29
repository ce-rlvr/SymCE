import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    try:
        h2 = bool(x in G and y in G)
    except Exception:
        h2 = False

    # H_3: xN and yN are conjugate in G/N
    try:
        h3 = False
        if h1 and h2:
            N_elements = set(N.generate())
            # Check if there exists g in G such that g*x*g^-1 * N == y * N
            # which is equivalent to y^-1 * g * x * g^-1 in N
            for g in G.generate():
                gxg = g * x * (~g)
                val = (~y) * gxg
                if val in N_elements:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: There does NOT exist n in N such that x is conjugate to yn in G
    try:
        neg_q = False
        if h1 and h2:
            # Compute the conjugacy class of x in G
            conj_class_x = set(h * x * (~h) for h in G.generate())
            
            # Assume true until we find a counterexample to the negation
            neg_q = True
            for n in N.generate():
                yn = y * n
                if yn in conj_class_x:
                    # Found an n where x is conjugate to yn in G (Conclusion holds)
                    # Therefore, the negated conclusion fails
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: x and y are elements of G",
    "H_3: xN and yN are conjugate in G/N",
    "¬Q: For all n in N, x is not conjugate to yn in G"
]

N_HYP = 3
NEG_Q_INDEX = 3