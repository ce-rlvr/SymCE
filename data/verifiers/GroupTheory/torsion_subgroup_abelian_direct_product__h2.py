import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class AbstractGroup:
    """
    A minimal class to represent abstract groups (especially infinite ones) 
    that cannot be easily represented by SymPy's PermutationGroup.
    """
    def __init__(self, name, is_abelian, is_torsion_set_subgroup):
        self.name = name
        self._is_abelian = is_abelian
        self._is_torsion_set_subgroup = is_torsion_set_subgroup

    @property
    def is_abelian(self):
        return self._is_abelian

    @property
    def is_torsion_set_subgroup(self):
        return self._is_torsion_set_subgroup

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

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

# Infinite groups for counterexamples
Z = AbstractGroup("Z", True, True)
Q_grp = AbstractGroup("Q", True, True)
R_grp = AbstractGroup("R", True, True)
D_inf = AbstractGroup("D_inf", False, False)
Free2 = AbstractGroup("Free2", False, True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple of two groups (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is an abelian group
    try:
        if hasattr(G, "is_abelian"):
            h1 = bool(G.is_abelian)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The torsion subgroup T(G x H) is equal to T(G) x T(H) FAILS
    try:
        def torsion_is_subgroup(grp):
            # If explicitly defined in our AbstractGroup
            if hasattr(grp, "is_torsion_set_subgroup"):
                return grp.is_torsion_set_subgroup
            # In any abelian group, the set of torsion elements forms a subgroup
            if hasattr(grp, "is_abelian") and grp.is_abelian:
                return True
            # In any finite group, all elements are torsion, so the set is the whole group (a subgroup)
            if isinstance(grp, PermutationGroup):
                return True
            # Default fallback
            return True
            
        # The conclusion holds if the set of torsion elements of G x H forms a subgroup,
        # AND the sets of torsion elements of G and H form subgroups.
        # Since Tor(G x H) = Tor(G) x Tor(H) as sets, it forms a subgroup iff both do.
        # If either does not form a subgroup, the term "torsion subgroup" is ill-defined,
        # and the equality of subgroups fails.
        q = torsion_is_subgroup(G) and torsion_is_subgroup(H)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The torsion subgroup T(G x H) is not equal to T(G) x T(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1