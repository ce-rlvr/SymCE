import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            return witness
        elif len(witness) == 3:
            F, H, n = witness
            if hasattr(H, 'index'):
                return F, H, n, H.index
            elif hasattr(H, 'k'):
                return F, H, n, H.k
    if hasattr(witness, 'F') and hasattr(witness, 'H') and hasattr(witness, 'n'):
        k = getattr(witness, 'k', getattr(witness.H, 'index', None))
        if k is not None:
            return witness.F, witness.H, witness.n, k
    if isinstance(witness, dict):
        if 'k' in witness:
            return witness['F'], witness['H'], witness['n'], witness['k']
        elif hasattr(witness.get('H'), 'index'):
            return witness['F'], witness['H'], witness['n'], witness['H'].index
    raise ValueError("Witness format not recognized")

def is_inf(val):
    if val == sympy.oo or val == -sympy.oo:
        return True
    try:
        return math.isinf(val)
    except Exception:
        return False

def is_nan(val):
    if val is sympy.nan:
        return True
    try:
        return math.isnan(val)
    except Exception:
        return False

def is_free_group(F):
    if type(F).__name__ == 'FreeGroup':
        return True
    if hasattr(F, 'is_free'):
        if callable(F.is_free):
            return F.is_free()
        return F.is_free
    return False

def get_F_rank(F):
    if hasattr(F, 'generators'):
        return len(F.generators)
    if hasattr(F, 'rank'):
        if callable(F.rank):
            return F.rank()
        return F.rank
    raise ValueError

def is_subgroup(H, F):
    if isinstance(H, (list, tuple)):
        if len(H) == 0:
            return True
        return all(getattr(h, 'group', None) == F for h in H)
    if hasattr(H, 'F'):
        return H.F is F or H.F == F
    if hasattr(H, 'is_subgroup_of'):
        return H.is_subgroup_of(F)
    return False

def get_H_rank(H):
    if isinstance(H, (list, tuple)):
        H_unique = []
        for h in H:
            if h not in H_unique:
                H_unique.append(h)
        if len(H_unique) == 0:
            return 0
        if len(H_unique) == 1:
            if hasattr(H_unique[0], 'group') and H_unique[0] == H_unique[0].group.identity:
                return 0
            return 1
        return len(H_unique)
    if hasattr(H, 'rank'):
        if callable(H.rank):
            return H.rank()
        return H.rank
    raise ValueError

def conditions(witness) -> list[bool]:
    try:
        F, H, n, k = extract(witness)
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group of finite rank n
    try:
        h1 = is_free_group(F) and get_F_rank(F) == n and not is_inf(n)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of F
    try:
        h2 = is_subgroup(H, F)
    except Exception:
        h2 = False
        
    # neg_Q: H is not a free group of finite rank equal to 1 + k(n - 1)
    try:
        rank_H = get_H_rank(H)
        if rank_H is None:
            neg_q = False
        else:
            if is_inf(rank_H):
                neg_q = True
            else:
                expected = 1 + k * (n - 1)
                if is_nan(expected):
                    neg_q = True
                else:
                    neg_q = (rank_H != expected)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank n",
    "H_2: H is a subgroup of F",
    "¬Q: H is not a free group of finite rank equal to 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2