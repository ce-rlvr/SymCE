import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _check_T_finite_char_subgroup(G, T):
    if T is not None:
        is_fin = True
        if hasattr(T, 'is_finite'):
            val = T.is_finite
            is_fin = bool(val() if callable(val) else val)
        
        is_char = True
        if hasattr(T, 'is_characteristic'):
            val = T.is_characteristic
            is_char = bool(val() if callable(val) else val)
            
        is_sub = True
        if hasattr(T, 'is_subgroup'):
            val = T.is_subgroup
            is_sub = bool(val() if callable(val) else val)
            
        return is_fin and is_char and is_sub
    else:
        if hasattr(G, 'has_finite_torsion_subgroup'):
            val = G.has_finite_torsion_subgroup
            return bool(val() if callable(val) else val)
        elif hasattr(G, 'torsion_subgroup_is_finite'):
            val = G.torsion_subgroup_is_finite
            return bool(val() if callable(val) else val)
        elif hasattr(G, 'torsion_subgroup'):
            ts = G.torsion_subgroup() if callable(G.torsion_subgroup) else G.torsion_subgroup
            if hasattr(ts, 'is_finite'):
                val = ts.is_finite
                return bool(val() if callable(val) else val)
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, T = witness
        else:
            G = witness
            T = None
    except Exception:
        G = witness
        T = None

    # H_1: G is a nilpotent group
    h1 = False
    try:
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # H_2: T is the set of all elements of finite order in G
    h2 = True
    try:
        if T is not None:
            if hasattr(T, 'is_set_of_finite_order_elements'):
                val = T.is_set_of_finite_order_elements
                h2 = bool(val(G) if callable(val) else val)
            elif hasattr(G, 'torsion_subgroup'):
                ts = G.torsion_subgroup() if callable(G.torsion_subgroup) else G.torsion_subgroup
                h2 = (T == ts)
    except Exception:
        h2 = False

    # neg_Q: T is NOT a finite characteristic subgroup of G
    q = True
    try:
        is_fin = None
        if hasattr(G, 'is_finite'):
            try:
                val = G.is_finite
                is_fin = bool(val() if callable(val) else val)
            except Exception:
                pass
        
        if is_fin is True:
            q = True
        else:
            q = _check_T_finite_char_subgroup(G, T)
    except Exception:
        q = True

    neg_q = not q

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: T is the set of all elements of finite order in G",
    "¬Q: T is not a finite characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2