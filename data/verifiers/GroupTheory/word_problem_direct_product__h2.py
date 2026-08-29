import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Standard algebra objects
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

# Mock objects for groups with specific word problem decidability
class MockGroup:
    def __init__(self, name, is_fg, has_swp):
        self.name = name
        self.is_finitely_generated = is_fg
        self.has_solvable_word_problem = has_swp
        
    def __str__(self):
        return self.name

Novikov_Boone_group = MockGroup("Novikov_Boone_group", is_fg=True, has_swp=False)
G_unsolvable = MockGroup("G_unsolvable", is_fg=True, has_swp=False)
G_solvable = MockGroup("G_solvable", is_fg=True, has_swp=True)


def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]

    def is_fg(grp):
        if hasattr(grp, 'is_finitely_generated'):
            return bool(grp.is_finitely_generated)
        if hasattr(grp, 'generators'):
            try:
                return len(list(grp.generators)) >= 0
            except Exception:
                pass
        return False

    def has_swp(grp):
        if hasattr(grp, 'has_solvable_word_problem'):
            return bool(grp.has_solvable_word_problem)
        if hasattr(grp, 'is_finite') and grp.is_finite:
            return True
        if hasattr(grp, 'generators'):
            # SymPy PermutationGroups are finite, hence have solvable word problems
            return True
        return False

    try:
        h1_ok = is_fg(G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_fg(H)
    except Exception:
        h2_ok = False

    try:
        h3_ok = has_swp(H)
    except Exception:
        h3_ok = False

    try:
        # The direct product G x H has a solvable word problem iff 
        # BOTH G and H have a solvable word problem.
        # The conclusion Q is that G x H has a solvable word problem.
        # We want neg_Q to be True when the conclusion FAILS.
        g_swp = has_swp(G)
        h_swp = has_swp(H)
        neg_q_ok = not (g_swp and h_swp)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]


CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: H is a finitely generated group",
    "H_3: H has a solvable word problem",
    "¬Q: The direct product G × H does not have a solvable word problem"
]

N_HYP = 3
NEG_Q_INDEX = 3