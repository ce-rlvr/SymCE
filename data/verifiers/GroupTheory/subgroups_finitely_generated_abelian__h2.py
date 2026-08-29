import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import S, eye, zeros

# Standard finite groups
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

# Standard matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Custom objects to represent infinite abelian groups that are not finitely generated
class InfiniteAbelianGroup:
    def __init__(self, name):
        self.name = name
        
    @property
    def is_abelian(self):
        return True
        
    @property
    def is_finitely_generated(self):
        return False
        
    def is_subgroup(self, other):
        return self == other

Q_plus = InfiniteAbelianGroup("Q_plus")
R_plus = InfiniteAbelianGroup("R_plus")
Q_mod_Z = InfiniteAbelianGroup("Q_mod_Z")

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is an abelian group
    try:
        h1 = False
        if isinstance(G, str) and G in ["Q", "R", "C", "Q/Z", "R/Z", "Z(p^infty)"]:
            h1 = True
        elif G in (S.Rationals, S.Reals, S.Complexes, S.Integers):
            h1 = True
        elif hasattr(G, "is_abelian"):
            h1 = bool(G.is_abelian)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = False
        if H == G:
            h2 = True
        elif isinstance(H, str) and isinstance(G, str):
            subs = {"Q": ["R", "C"], "R": ["C"], "Z": ["Q", "R", "C"]}
            if G in subs.get(H, []):
                h2 = True
        elif H in (S.Rationals, S.Reals, S.Complexes, S.Integers) and G in (S.Rationals, S.Reals, S.Complexes, S.Integers):
            subs = {
                S.Integers: [S.Rationals, S.Reals, S.Complexes], 
                S.Rationals: [S.Reals, S.Complexes], 
                S.Reals: [S.Complexes]
            }
            if G in subs.get(H, []):
                h2 = True
        elif hasattr(H, "is_subgroup"):
            h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False

    # ¬Q: H is NOT finitely generated
    try:
        neg_q = False
        if isinstance(H, str):
            if H in ["Q", "R", "C", "Q/Z", "R/Z", "Z(p^infty)"]:
                neg_q = True
        elif H in (S.Rationals, S.Reals, S.Complexes):
            neg_q = True
        elif H == S.Integers:
            neg_q = False
        elif hasattr(H, "is_finitely_generated"):
            neg_q = not bool(H.is_finitely_generated)
        elif type(H).__name__ in ["PermutationGroup", "FpGroup"]:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2