import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
            n = witness.get('n')
            k = witness.get('k')
        elif isinstance(witness, (tuple, list)):
            F, H, n, k = witness
        else:
            F = witness.F
            H = witness.H
            n = witness.n
            k = witness.k
    except Exception:
        return [False, False, False]

    # H1: F is a free group of finite rank n
    try:
        h1 = False
        is_free = type(F).__name__ in ['FreeGroup', 'FpGroup'] or getattr(F, 'is_free_group', False)
        if is_free and getattr(F, 'rank', None) == n and isinstance(n, int) and not isinstance(n, bool):
            h1 = True
    except Exception:
        h1 = False

    # H2: The index of H in F is a finite integer k
    try:
        h2 = False
        idx = None
        if hasattr(F, 'index'):
            idx = F.index(H)
        elif hasattr(H, 'index_in'):
            idx = H.index_in(F)
        elif hasattr(H, 'index'):
            idx = H.index(F)
        elif isinstance(witness, dict) and 'index' in witness:
            idx_val = witness['index']
            if callable(idx_val):
                idx = idx_val(F, H)
            else:
                idx = idx_val
        elif hasattr(witness, 'index'):
            if callable(witness.index):
                idx = witness.index(F, H)
            else:
                idx = witness.index
            
        if idx == k and isinstance(k, int) and not isinstance(k, bool):
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: H is not a free group of finite rank equal to 1 + k(n - 1)
    try:
        expected_rank = 1 + k * (n - 1)
        q = False
        is_h_free = type(H).__name__ in ['FreeGroup', 'FpGroup', 'FpSubgroup'] or getattr(H, 'is_free_group', False)
        if is_h_free and getattr(H, 'rank', None) == expected_rank:
            q = True
        neg_q = not q
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "H_2: The index of H in F is a finite integer k",
    "¬Q: H is not a free group of finite rank equal to 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2