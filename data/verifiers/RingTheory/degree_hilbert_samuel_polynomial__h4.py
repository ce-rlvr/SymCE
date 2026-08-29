import sympy
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup
# No specific named objects are required for this abstract ring theory conjecture,
# but we provide standard symbols just in case the witness uses them.
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    # If witness is a tuple/list of 4 booleans
    if isinstance(witness, (tuple, list)) and len(witness) == 4:
        try:
            return [bool(w) for w in witness]
        except Exception:
            pass

    def get_val(obj, keys):
        if isinstance(obj, dict):
            for k in keys:
                if k in obj: return obj[k]
        else:
            for k in keys:
                if hasattr(obj, k): return getattr(obj, k)
        return None

    # H1: (R, m) is a commutative Noetherian local ring
    try:
        is_comm = get_val(witness, ['is_commutative', 'is_commutative_ring'])
        is_noeth = get_val(witness, ['is_Noetherian', 'is_noetherian'])
        is_loc = get_val(witness, ['is_local', 'is_local_ring'])
        if is_comm is not None and is_noeth is not None and is_loc is not None:
            h1 = bool(is_comm and is_noeth and is_loc)
        else:
            val = get_val(witness, ['is_commutative_Noetherian_local_ring', 'h1'])
            if val is not None: 
                h1 = bool(val)
    except Exception:
        h1 = False

    # H2: d is the Krull dimension of R
    try:
        d = get_val(witness, ['d', 'dim'])
        krull = get_val(witness, ['Krull_dimension', 'krull_dimension'])
        if d is not None and krull is not None:
            h2 = bool(d == krull)
        elif d is not None or krull is not None:
            h2 = True
        else:
            val = get_val(witness, ['d_is_Krull_dimension', 'h2'])
            if val is not None: 
                h2 = bool(val)
    except Exception:
        h2 = False

    # H3: I is an m-primary ideal of R
    try:
        val = get_val(witness, ['I_is_m_primary', 'is_m_primary', 'h3'])
        if val is not None:
            h3 = bool(val)
        else:
            I = get_val(witness, ['I'])
            m = get_val(witness, ['m'])
            if I is not None and m is not None:
                h3 = bool(getattr(I, 'is_primary', False) and getattr(I, 'radical', None) == m)
    except Exception:
        h3 = False

    # ¬Q: The degree of the polynomial P_I(n) is not exactly d
    try:
        deg = get_val(witness, ['P_I_degree', 'degree_P_I', 'degree'])
        d = get_val(witness, ['d', 'dim'])
        if deg is not None and d is not None:
            neg_q = bool(deg != d)
        else:
            val = get_val(witness, ['degree_P_I_not_d', 'neg_q'])
            if val is not None: 
                neg_q = bool(val)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: d is the Krull dimension of R",
    "H_3: I is an m-primary ideal of R",
    "¬Q: The degree of the polynomial P_I(n) is not exactly d"
]

N_HYP = 3
NEG_Q_INDEX = 3