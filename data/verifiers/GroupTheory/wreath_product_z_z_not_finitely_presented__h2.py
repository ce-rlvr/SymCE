import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_Z(group):
    if isinstance(group, str):
        g_str = group.strip().lower()
        if g_str in ['z', 'z1', 'integers', 'infinite cyclic', 'infinite cyclic group']:
            return True
    try:
        if hasattr(group, 'generators') and len(group.generators) == 1:
            if hasattr(group, 'relators') and len(group.relators) == 0:
                return True
            if not hasattr(group, 'relators'):
                return True
    except Exception:
        pass
    return False

def is_trivial(group):
    if isinstance(group, str):
        g_str = group.strip().lower()
        if g_str in ['1', 'trivial', 'trivial group', 'e', 'id', 'c1', 'z1']:
            return True
    try:
        if hasattr(group, 'order') and group.order() == 1:
            return True
    except Exception:
        pass
    try:
        if hasattr(group, 'elements') and len(list(group.elements)) == 1:
            return True
    except Exception:
        pass
    return False

def is_finite(group):
    if isinstance(group, str):
        g_str = group.strip().lower()
        if g_str in ['1', 'trivial', 'e', 'z2', 'z3', 'z4', 'z6', 's3', 's4', 'a4', 'd4', 'v4', 'c4']:
            return True
        if 'finite' in g_str:
            return True
    try:
        if hasattr(group, 'order'):
            ord_g = group.order()
            if ord_g < float('inf'):
                return True
    except Exception:
        pass
    try:
        if hasattr(group, 'is_finite') and group.is_finite:
            return True
    except Exception:
        pass
    return False

def is_wreath(G, A, B):
    if is_trivial(B) and is_Z(G) and is_Z(A):
        return True
    if isinstance(G, str):
        g_str = G.strip().lower().replace(' ', '')
        a_str = str(A).strip().lower().replace(' ', '')
        b_str = str(B).strip().lower().replace(' ', '')
        if g_str == f"{a_str}wr{b_str}":
            return True
        if g_str == f"wreath({a_str},{b_str})":
            return True
        if 'wr' in g_str:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A', 'Z')
            B = witness.get('B', 'trivial')
            G = witness.get('G', 'Z')
        elif isinstance(witness, tuple) and len(witness) == 3:
            A, B, G = witness
        else:
            B = witness
            A = 'Z'
            if is_trivial(B):
                G = 'Z'
            else:
                G = f"Z wr {B}"
    except Exception:
        return [False, False, False]

    # H1: A is the infinite cyclic group Z
    try:
        h1 = is_Z(A)
    except Exception:
        h1 = False

    # H2: G is the restricted wreath product A wr B
    try:
        h2 = is_wreath(G, A, B)
    except Exception:
        h2 = False

    # Q: G is finitely generated but not finitely presented
    try:
        if is_trivial(B):
            fg = True
            fp = True
        elif is_finite(B):
            fg = True
            fp = True
        elif is_Z(B):
            fg = True
            fp = False
        else:
            # Fallback
            fg = True
            fp = False
            if isinstance(G, str) and 'wr' not in G.lower():
                fp = True
        
        q = fg and not fp
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is the infinite cyclic group Z",
    "H_2: G is the restricted wreath product A wr B",
    "¬Q: G is either not finitely generated or is finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2