import sympy
from sympy import ZZ, QQ
from sympy.polys.rings import ring

# Top-level setup for witness expressions
Z = ZZ
Q = QQ
Zx, x_Z = ring('x', ZZ)
Qx, x_Q = ring('x', QQ)
x = sympy.Symbol('x')

S_1 = {1}
S_units = {1, -1}

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            M = witness.get('M')
        else:
            R, S, M = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in [ZZ, QQ, Zx, Qx, sympy.S.Integers, sympy.S.Rationals]:
            h1 = True
        elif isinstance(R, str) and R in ['Z', 'Q', 'Z[x]', 'Q[x]', 'R']:
            h1 = True
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        h2 = False
        if isinstance(S, (set, list, tuple)) and len(S) > 0:
            h2 = True
            for a in S:
                for b in S:
                    try:
                        if (a * b) not in S:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
                if not h2:
                    break
        elif isinstance(S, str) and S in ['{1}', 'Z\\{0}', 'S_1', 'S_units']:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: S^{-1}M is NOT a finitely generated S^{-1}R-module
    try:
        neg_q = False
        
        is_R_Z = R in [ZZ, sympy.S.Integers] or (isinstance(R, str) and R == 'Z')
        is_R_Q = R in [QQ, sympy.S.Rationals] or (isinstance(R, str) and R == 'Q')
        
        is_M_Q = M in [QQ, sympy.S.Rationals] or (isinstance(M, str) and M in ['Q', 'Rationals'])
        is_M_Zx = M == Zx or (isinstance(M, str) and M in ['Z[x]', 'Z[X]'])
        is_M_Qx = M == Qx or (isinstance(M, str) and M in ['Q[x]', 'Q[X]'])
        is_M_Q_Z = isinstance(M, str) and M in ['Q/Z', 'Q / Z']
        
        is_S_trivial = False
        if isinstance(S, (set, list, tuple)):
            if set(S) == {1} or set(S) == {1, -1}:
                is_S_trivial = True
        elif isinstance(S, str) and S in ['{1}', 'S_1', 'S_units']:
            is_S_trivial = True
        
        if is_S_trivial:
            if is_R_Z and (is_M_Q or is_M_Zx or is_M_Qx or is_M_Q_Z):
                neg_q = True
            if is_R_Q and is_M_Qx:
                neg_q = True
                
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}M is not a finitely generated S^{-1}R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2