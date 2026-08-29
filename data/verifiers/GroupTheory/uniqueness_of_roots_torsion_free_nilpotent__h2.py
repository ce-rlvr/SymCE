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

CONDITION_LABELS = [
    "H_1: G is a torsion-free nilpotent group",
    "H_2: n is a non-zero integer such that x^n = y^n",
    "¬Q: x != y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
            n = witness.get('n')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            G, x, y, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a torsion-free nilpotent group
    h1 = False
    try:
        if hasattr(G, '__contains__'):
            if x not in G or y not in G:
                raise ValueError("Elements not in G")
                
        is_nilp = False
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            is_nilp = val() if callable(val) else val
        elif hasattr(G, 'is_abelian'):
            val = G.is_abelian
            is_nilp = val() if callable(val) else val
        
        is_tf = False
        if hasattr(G, 'is_torsion_free'):
            val = G.is_torsion_free
            is_tf = val() if callable(val) else val
        elif hasattr(G, 'order'):
            val = G.order
            order = val() if callable(val) else val
            if order == 1:
                is_tf = True
        elif G.__class__.__name__ == 'FreeGroup':
            is_tf = True
            
        if is_nilp and is_tf:
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a non-zero integer such that x^n = y^n
    h2 = False
    try:
        if isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer):
            n_val = int(n)
            if n_val != 0:
                if bool(x**n_val == y**n_val):
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: x != y
    neg_q = False
    try:
        neg_q = not bool(x == y)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]