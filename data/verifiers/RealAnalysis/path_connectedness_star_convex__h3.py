import sympy

# Top-level setup
# (No specific named objects needed for this real analysis theorem)

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, S_set = witness
        else:
            n = 1
            S_set = witness
            
        # H_1: n is a positive integer
        try:
            h1_ok = isinstance(n, (int, sympy.Integer)) and n > 0
        except Exception:
            h1_ok = False
            
        # H_2: S is a subset of R^n
        try:
            if n == 1:
                h2_ok = (S_set.is_subset(sympy.S.Reals) == True)
            else:
                h2_ok = (S_set.is_subset(sympy.S.Reals ** n) == True)
        except Exception:
            h2_ok = False
            
        # ¬Q: S is not path-connected
        try:
            def is_path_connected(S_obj, dim):
                if dim == 1:
                    if isinstance(S_obj, sympy.Interval):
                        return True
                    if S_obj == sympy.S.Reals:
                        return True
                    if S_obj == sympy.S.EmptySet:
                        return True
                    if isinstance(S_obj, sympy.FiniteSet) and len(S_obj) <= 1:
                        return True
                    return False
                else:
                    if isinstance(S_obj, sympy.ProductSet):
                        return all(is_path_connected(arg, 1) for arg in S_obj.args)
                    if isinstance(S_obj, sympy.FiniteSet) and len(S_obj) <= 1:
                        return True
                    return False
            
            neg_q_ok = not is_path_connected(S_set, n)
        except Exception:
            neg_q_ok = False
            
    except Exception:
        pass
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: S is a subset of R^n",
    "¬Q: S is not path-connected"
]

N_HYP = 2
NEG_Q_INDEX = 2