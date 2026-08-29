import sympy
from sympy.polys.domains import QQ, ZZ, Domain
from sympy.polys.agca.modules import FreeModule, SubModule

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a free module over R",
    "¬Q: M contains a non-zero divisible submodule"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, M, N = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is an integral domain
    try:
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False
        
    # H_2: M is a free module over R
    try:
        h2 = isinstance(M, FreeModule) and M.ring == R
    except Exception:
        h2 = False
        
    # ¬Q: M contains a non-zero divisible submodule (witnessed by N)
    try:
        is_submod = False
        is_nonzero = False
        
        if isinstance(N, FreeModule) and N == M:
            is_submod = True
            is_nonzero = (M.rank > 0)
        elif isinstance(N, SubModule):
            if getattr(N, 'container', None) == M:
                is_submod = True
            else:
                try:
                    is_submod = all(gen in M for gen in N.gens)
                except Exception:
                    is_submod = False
            
            if is_submod:
                for gen in N.gens:
                    for c in gen:
                        if c != 0:
                            is_nonzero = True
                            break
                    if is_nonzero:
                        break
                        
        # A non-zero submodule of a free module over an integral domain R
        # is divisible if and only if R is a field.
        is_divisible = bool(R.is_Field)
        
        neg_q = is_submod and is_nonzero and is_divisible
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]