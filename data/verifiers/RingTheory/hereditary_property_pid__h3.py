import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_pid(R):
    try:
        if isinstance(R, str):
            R_str = R.replace(' ', '')
            if R_str in ('Z', 'ZZ', 'Q', 'QQ', 'R', 'RR', 'C', 'CC', 'Q[x]', 'QQ[x]', 'R[x]', 'RR[x]', 'C[x]', 'CC[x]', 'Z[i]'):
                return True
            if R_str in ('Z[x]', 'ZZ[x]', 'Q[x,y]', 'Z[x,y]'):
                return False
        
        from sympy import ZZ, QQ
        from sympy.polys.domains import ZZ as poly_ZZ, QQ as poly_QQ
        if R in (ZZ, QQ, poly_ZZ, poly_QQ):
            return True
        
        if hasattr(R, 'is_PID'):
            return bool(R.is_PID)
        if hasattr(R, 'is_PrincipalIdealDomain'):
            return bool(R.is_PrincipalIdealDomain)
    except Exception:
        pass
    return False

def check_projective(R, mod):
    try:
        if isinstance(mod, str):
            mod_str = mod.replace(' ', '')
            R_str = str(R).replace(' ', '')
            if mod_str == R_str or mod_str == '0':
                return True
            if mod_str in ('Z', 'ZZ') and R_str in ('Z', 'ZZ'):
                return True
            if mod_str in ('Q', 'QQ') and R_str in ('Q', 'QQ'):
                return True
            return False

        if hasattr(mod, 'smith_normal_form'):
            snf = mod.smith_normal_form()
            diag = [snf[i, i] for i in range(min(snf.rows, snf.cols))]
            mod = diag
        
        if isinstance(mod, (list, tuple)):
            for val in mod:
                if val == 0:
                    continue
                try:
                    int_val = int(val)
                    if abs(int_val) > 1:
                        return False
                except Exception:
                    from sympy import degree
                    try:
                        if degree(val) > 0:
                            return False
                    except Exception:
                        return False
            return True
        elif isinstance(mod, int):
            return abs(mod) <= 1
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            P = witness.get('P')
            M = witness.get('M')
        elif hasattr(witness, 'R') and hasattr(witness, 'P') and hasattr(witness, 'M'):
            R = witness.R
            P = witness.P
            M = witness.M
        else:
            R, P, M = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = is_pid(R)
    except Exception:
        h1 = False

    try:
        h2 = check_projective(R, P)
    except Exception:
        h2 = False

    try:
        neg_q = not check_projective(R, M)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: P is a projective R-module",
    "¬Q: M is not a projective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2