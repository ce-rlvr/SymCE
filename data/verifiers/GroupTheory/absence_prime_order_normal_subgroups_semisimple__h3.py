import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import sympy.ntheory

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, p, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: Let G be a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a semisimple group
    # A finite group is semisimple iff it has no non-trivial abelian normal subgroups.
    # This is equivalent to saying that for every non-identity element g in G,
    # the normal closure of <g> in G is not abelian.
    try:
        if h1:
            has_abelian_normal = False
            for g in G.elements:
                if not g.support():  # Check if g is the identity permutation
                    continue
                H = PermutationGroup([g])
                N_closure = G.normal_closure(H)
                if N_closure.is_abelian:
                    has_abelian_normal = True
                    break
            h2 = not has_abelian_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: Let p be a prime number
    try:
        h3 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h3 = False

    # ¬Q: The order of the subgroup N is equal to p
    try:
        if isinstance(N, PermutationGroup) and h1:
            # Verify N is actually a subgroup of G
            is_sub = all((g in G) for g in N.generators)
            neg_q = is_sub and (N.order() == p)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: p is a prime number",
    "¬Q: The order of the subgroup N is equal to p"
]

N_HYP = 3
NEG_Q_INDEX = 3