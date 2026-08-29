import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ
Zx = ZZ['x']
Qx = QQ['x']

def check_is_mod(M, R):
    if M == R:
        return True
    if R == sympy.ZZ and M == sympy.QQ:
        return True
    if hasattr(M, 'domain'):
        if M.domain == R:
            return True
        if check_is_mod(M.domain, R):
            return True
    return False

def check_is_noeth(M, R):
    if M == R:
        return True
    if R == sympy.ZZ and M == sympy.QQ:
        return False
    if hasattr(M, 'domain'):
        if M.domain == R:
            if hasattr(M, 'gens') and len(M.gens) > 0:
                return False
        elif check_is_mod(M.domain, R):
            if hasattr(M, 'gens') and len(M.gens) > 0:
                return False
            if check_is_noeth(M.domain, R) is False:
                return False
    return None

def conditions(witness) -> list[bool]:
    try:
        R, n, M_list = witness
        if R == sympy.S.Integers:
            R = sympy.ZZ
        elif R == sympy.S.Rationals:
            R = sympy.QQ
        elif R == sympy.S.Reals:
            R = sympy.RR
        elif R == sympy.S.Complexes:
            R = sympy.CC
    except Exception:
        return [False, False, False]
        
    # H_1: R is a ring
    try:
        from sympy.polys.domains.ring import Ring
        h1 = isinstance(R, Ring)
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False
        
    # neg_Q: The finite direct sum is NOT a Noetherian R-module
    try:
        if not isinstance(M_list, (list, tuple)):
            neg_q = False
        elif len(M_list) != n:
            neg_q = False
        else:
            translated_M_list = []
            for M in M_list:
                if M == sympy.S.Integers: M = sympy.ZZ
                elif M == sympy.S.Rationals: M = sympy.QQ
                elif M == sympy.S.Reals: M = sympy.RR
                elif M == sympy.S.Complexes: M = sympy.CC
                translated_M_list.append(M)
            M_list = translated_M_list

            all_valid_modules = True
            has_non_noetherian = False
            for M in M_list:
                if not check_is_mod(M, R):
                    all_valid_modules = False
                    break
                
                if check_is_noeth(M, R) is False:
                    has_non_noetherian = True
            
            neg_q = all_valid_modules and has_non_noetherian
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: n is a positive integer",
    "¬Q: The finite direct sum is NOT a Noetherian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2