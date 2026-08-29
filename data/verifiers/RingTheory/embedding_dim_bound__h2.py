import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(w, names):
    if isinstance(w, dict):
        for name in names:
            if name in w:
                return w[name]
    else:
        for name in names:
            if hasattr(w, name):
                val = getattr(w, name)
                if callable(val):
                    return val()
                return val
    return None

def conditions(witness):
    try:
        is_noeth = get_attr(witness, ['is_noetherian', 'noetherian'])
        is_local = get_attr(witness, ['is_local', 'local'])
        h1_ok = bool(is_noeth) and bool(is_local)
    except Exception:
        h1_ok = False

    try:
        emb_dim = get_attr(witness, ['embedding_dimension', 'emb_dim', 'm_mod_m2_dim', 'dim_m_m2'])
        krull_dim = get_attr(witness, ['krull_dimension', 'krull_dim', 'dim'])
        
        if emb_dim is None or krull_dim is None:
            neg_q_ok = False
        else:
            is_finite = True
            if emb_dim == float('inf') or emb_dim == math.inf or emb_dim == sympy.oo or str(emb_dim).lower() in ['inf', 'infinity']:
                is_finite = False
            
            if not is_finite:
                neg_q_ok = True
            else:
                neg_q_ok = bool(emb_dim < krull_dim)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Noetherian local ring with maximal ideal m",
    "¬Q: The vector space dimension of m/m^2 over k is infinite or strictly less than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1