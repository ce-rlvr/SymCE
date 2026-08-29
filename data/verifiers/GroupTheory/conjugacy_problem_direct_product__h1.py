import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_scp(g):
    """Helper to check if a group has a solvable conjugacy problem."""
    if isinstance(g, dict) and 'has_solvable_conjugacy_problem' in g:
        v = g['has_solvable_conjugacy_problem']
        return v() if callable(v) else bool(v)
    if hasattr(g, 'has_solvable_conjugacy_problem'):
        v = g.has_solvable_conjugacy_problem
        return v() if callable(v) else bool(v)
    if hasattr(g, 'is_finite'):
        v = g.is_finite
        if callable(v): 
            v = v()
        if v: 
            return True
    return False

def get_fg(g):
    """Helper to check if a group is finitely generated."""
    if isinstance(g, dict) and 'is_finitely_generated' in g:
        v = g['is_finitely_generated']
        return v() if callable(v) else bool(v)
    if hasattr(g, 'is_finitely_generated'):
        v = g.is_finitely_generated
        return v() if callable(v) else bool(v)
    if isinstance(g, PermutationGroup):
        return True
    return False

def conditions(witness) -> list[bool]:
    # Extract G, H, and optionally GxH from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            GxH = witness.get('GxH', None)
        elif isinstance(witness, (tuple, list)):
            G = witness[0]
            H = witness[1]
            GxH = witness[2] if len(witness) > 2 else None
        else:
            G = witness.G
            H = witness.H
            GxH = getattr(witness, 'GxH', None)
    except Exception:
        return [False, False, False, False]

    # H_1: G has a solvable conjugacy problem
    try:
        h1 = get_scp(G)
    except Exception:
        h1 = False

    # H_2: H is a finitely generated group
    try:
        h2 = get_fg(H)
    except Exception:
        h2 = False

    # H_3: H has a solvable conjugacy problem
    try:
        h3 = get_scp(H)
    except Exception:
        h3 = False

    # ¬Q: The direct product G x H does NOT have a solvable conjugacy problem
    try:
        if GxH is None:
            if hasattr(G, 'direct_product'):
                GxH = G.direct_product(H)
            elif hasattr(G, '__mul__'):
                GxH = G * H
            else:
                neg_q = False
        
        if GxH is not None:
            neg_q = not get_scp(GxH)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G has a solvable conjugacy problem",
    "H_2: H is a finitely generated group",
    "H_3: H has a solvable conjugacy problem",
    "¬Q: The direct product G x H does not have a solvable conjugacy problem"
]

N_HYP = 3
NEG_Q_INDEX = 3
