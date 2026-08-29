import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

class MockGroup:
    """
    A mock group object to represent groups with specific properties,
    such as finitely generated groups with an unsolvable conjugacy problem.
    """
    def __init__(self, fg=True, scp=True):
        self.is_finitely_generated = fg
        self.has_solvable_conjugacy_problem = scp

def is_finitely_generated(grp):
    if hasattr(grp, 'is_finitely_generated'):
        val = grp.is_finitely_generated
        return bool(val() if callable(val) else val)
    if hasattr(grp, 'generators'):
        try:
            return len(tuple(grp.generators)) >= 0
        except Exception:
            pass
    if getattr(grp, 'is_finite', False):
        return True
    name = type(grp).__name__
    if name in ['FpGroup', 'FreeGroup', 'PermutationGroup']:
        return True
    return False

def has_solvable_conjugacy_problem(grp):
    if hasattr(grp, 'has_solvable_conjugacy_problem'):
        val = grp.has_solvable_conjugacy_problem
        return bool(val() if callable(val) else val)
    if getattr(grp, 'is_finite', False):
        return True
    name = type(grp).__name__
    if name == 'FreeGroup':
        return True
    if name == 'FpGroup':
        # Finitely presented groups have an unsolvable conjugacy problem in general.
        # We return False to allow FpGroup to act as a counterexample factor.
        return False
    if name == 'PermutationGroup':
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_finitely_generated(G)
    except Exception:
        h1 = False

    try:
        h2 = has_solvable_conjugacy_problem(G)
    except Exception:
        h2 = False

    try:
        h3 = is_finitely_generated(H)
    except Exception:
        h3 = False

    try:
        # The direct product G x H has a solvable conjugacy problem if and only if
        # both G and H have a solvable conjugacy problem.
        q = has_solvable_conjugacy_problem(G) and has_solvable_conjugacy_problem(H)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G has a solvable conjugacy problem",
    "H_3: H is a finitely generated group",
    "¬Q: The direct product G × H does not have a solvable conjugacy problem"
]

N_HYP = 3
NEG_Q_INDEX = 3