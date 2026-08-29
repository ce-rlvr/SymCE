import sympy

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should provide the ring R, the module F, the submodule M, and the rank n.
    For simplicity, modules over Z are represented by a list of their invariant factors.
    0 represents a free component Z, 1 represents the trivial component 0, 
    and k > 1 represents Z/kZ.
    
    Example witness:
    witness = {
        'R': 'Z',
        'F': [2], # F = Z/2Z
        'M': [2], # M = Z/2Z
        'n': 1
    }
    """
    try:
        h1 = False
        h2 = False
        neg_q = False
        
        def get_val(key):
            if isinstance(witness, dict) and key in witness:
                return witness[key]
            if hasattr(witness, key):
                return getattr(witness, key)
            return None

        # H_1: R is a principal ideal domain
        R = get_val('R')
        if R == 'Z' or R == sympy.S.Integers:
            h1 = True
            
        # H_2: M is a submodule of F
        M = get_val('M')
        F = get_val('F')
        
        if isinstance(M, list) and isinstance(F, list):
            M_non_trivial = [m for m in M if m != 1]
            F_available = list(F)
            
            is_sub = True
            for m in M_non_trivial:
                if not isinstance(m, int) or m < 0:
                    is_sub = False
                    break
                matched = False
                for i, f in enumerate(F_available):
                    if not isinstance(f, int) or f < 0:
                        continue
                    if f == 0:
                        if m == 0:
                            matched = True
                            F_available.pop(i)
                            break
                    else:
                        if m != 0 and f % m == 0:
                            matched = True
                            F_available.pop(i)
                            break
                if not matched:
                    is_sub = False
                    break
            
            if is_sub:
                for f in F:
                    if not isinstance(f, int) or f < 0:
                        is_sub = False
                        break
            
            h2 = is_sub

        # ¬Q: M is not a free R-module of rank less than or equal to n
        n = get_val('n')
        if isinstance(M, list) and isinstance(n, int):
            is_free = True
            for m in M:
                if m != 0 and m != 1:
                    is_free = False
                    break
            
            if not is_free:
                neg_q = True
            else:
                rank = sum(1 for m in M if m == 0)
                if rank > n:
                    neg_q = True

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a submodule of F",
    "¬Q: M is not a free R-module of rank less than or equal to n"
]

N_HYP = 2
NEG_Q_INDEX = 2