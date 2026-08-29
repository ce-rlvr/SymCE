import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DirectProduct(CyclicGroup(2), CyclicGroup(2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of three groups (A, B, C).
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        A, B, C = witness
    except Exception:
        return [False, False, False, False]

    # Helper to allow lists of integers to represent direct products of cyclic groups
    def to_group(G):
        if isinstance(G, int) and G > 0:
            return CyclicGroup(G)
        if isinstance(G, list):
            if not G:
                return CyclicGroup(1)
            groups = []
            for n in G:
                if isinstance(n, int) and n > 0:
                    groups.append(CyclicGroup(n))
                else:
                    return G
            if len(groups) == 1:
                return groups[0]
            return DirectProduct(*groups)
        return G

    try:
        A = to_group(A)
        B = to_group(B)
        C = to_group(C)
    except Exception:
        pass

    # H1: A is a finite abelian group
    try:
        h1 = bool(A.is_abelian and A.order() != sympy.oo and A.order() > 0)
    except Exception:
        h1 = False

    # H2: B is a finite abelian group
    try:
        h2 = bool(B.is_abelian and B.order() != sympy.oo and B.order() > 0)
    except Exception:
        h2 = False

    # H3: The direct sum A ⊕ B is isomorphic to A ⊕ C
    try:
        AxB = DirectProduct(A, B)
        AxC = DirectProduct(A, C)
        if AxB.is_abelian and AxC.is_abelian:
            h3 = sorted(AxB.abelian_invariants()) == sorted(AxC.abelian_invariants())
        elif not AxB.is_abelian and not AxC.is_abelian:
            h3 = bool(AxB.is_isomorphic(AxC))
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The group B is not isomorphic to the group C
    try:
        if B.is_abelian and getattr(C, 'is_abelian', False):
            neg_q = sorted(B.abelian_invariants()) != sorted(C.abelian_invariants())
        elif not B.is_abelian and not getattr(C, 'is_abelian', False):
            neg_q = not bool(B.is_isomorphic(C))
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: B is a finite abelian group",
    "H_3: The direct sum A ⊕ B is isomorphic to A ⊕ C",
    "¬Q: The group B is not isomorphic to the group C"
]

N_HYP = 3
NEG_Q_INDEX = 3