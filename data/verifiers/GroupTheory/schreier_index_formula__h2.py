import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "H_2: H has finite index k in F",
    "¬Q: H is not a free group of rank 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract F, H, n, k from the witness
    F, H, n, k = None, None, None, None
    if isinstance(witness, dict):
        F = witness.get('F')
        H = witness.get('H')
        n = witness.get('n')
        k = witness.get('k')
    elif isinstance(witness, tuple) and len(witness) == 4:
        F, H, n, k = witness
    else:
        F = getattr(witness, 'F', None)
        H = getattr(witness, 'H', None)
        n = getattr(witness, 'n', None)
        k = getattr(witness, 'k', None)

    # H_1: F is a free group of finite rank n
    h1 = False
    try:
        if type(F).__name__ == 'FreeGroup':
            h1 = (F.rank == n)
        elif isinstance(F, dict):
            h1 = (F.get('is_free_group', False) and F.get('rank') == n)
        elif hasattr(F, 'is_free_group'):
            h1 = (F.is_free_group and getattr(F, 'rank', None) == n)
        elif hasattr(F, 'relators') and hasattr(F, 'generators'):
            if len(F.relators) == 0:
                h1 = (len(F.generators) == n)
    except Exception:
        h1 = False

    # H_2: H has finite index k in F
    h2 = False
    try:
        if isinstance(H, dict):
            h2 = (H.get('index') == k)
        elif hasattr(H, 'index'):
            if callable(H.index):
                try:
                    idx = H.index(F)
                except Exception:
                    idx = H.index()
            else:
                idx = H.index
            h2 = (idx == k)
        elif hasattr(H, 'index_in'):
            h2 = (H.index_in(F) == k)
        elif hasattr(F, 'index'):
            if callable(F.index):
                h2 = (F.index(H) == k)
    except Exception:
        h2 = False

    # ¬Q: H is NOT a free group of rank 1 + k(n - 1)
    neg_q = False
    try:
        if n is None or k is None:
            raise ValueError("n or k is missing")
            
        expected_rank = 1 + k * (n - 1)
        is_free = False
        rank = None
        
        if type(H).__name__ == 'FreeGroup':
            is_free = True
            rank = H.rank
        elif isinstance(H, dict):
            is_free = H.get('is_free_group', False)
            rank = H.get('rank', None)
        elif hasattr(H, 'is_free_group'):
            is_free = H.is_free_group
            rank = getattr(H, 'rank', None)
        elif hasattr(H, 'relators') and hasattr(H, 'generators'):
            if len(H.relators) == 0:
                is_free = True
                rank = len(H.generators)
                
        if is_free and rank == expected_rank:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]