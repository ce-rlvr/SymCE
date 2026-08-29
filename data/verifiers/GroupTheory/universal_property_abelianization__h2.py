import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        G, A, f = witness
    except Exception:
        return [False, False, False]

    # H1: G and A are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(A, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f is a group homomorphism from G to A
    try:
        h2 = False
        if h1:
            is_hom = True
            elements_G = list(G.elements)
            set_A = set(A.elements)
            for x in elements_G:
                fx = f(x) if callable(f) else f[x]
                if fx not in set_A:
                    is_hom = False
                    break
            if is_hom:
                for x in elements_G:
                    for y in elements_G:
                        fx = f(x) if callable(f) else f[x]
                        fy = f(y) if callable(f) else f[y]
                        fxy = f(x*y) if callable(f) else f[x*y]
                        if fxy != fx * fy:
                            is_hom = False
                            break
                    if not is_hom:
                        break
            h2 = is_hom
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails (f does not factor through G/G', i.e., G' is not in ker(f))
    try:
        neg_q = False
        if h1 and h2:
            G_prime = G.derived_subgroup()
            identity_A = list(A.elements)[0]**0
            for x in G_prime.elements:
                fx = f(x) if callable(f) else f[x]
                if fx != identity_A:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and A are groups",
    "H_2: f is a group homomorphism from G to A",
    "¬Q: There does not exist a unique homomorphism f~: G/G' -> A such that f = f~ o pi"
]

N_HYP = 2
NEG_Q_INDEX = 2