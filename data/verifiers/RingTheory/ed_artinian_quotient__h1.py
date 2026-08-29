import sympy
from sympy import groebner, Poly
from sympy.abc import x, y, z, u, v, w

# Top-level setup
# The witness is expected to be a tuple: (vars, gens)
# where `vars` is a list of SymPy symbols (e.g., [x, y])
# and `gens` is a list of SymPy expressions generating the ideal I in the polynomial ring QQ[vars].
# Example witness: ([x, y], [x])

def conditions(witness) -> list[bool]:
    try:
        vars, gens = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: I is a non-zero proper ideal of R
        is_nonzero = False
        for g in gens:
            if not Poly(g, *vars, domain='QQ').is_zero:
                is_nonzero = True
                break
        
        is_proper = True
        if is_nonzero:
            gb = groebner(gens, *vars, domain='QQ')
            for g in gb:
                p = Poly(g, *vars, domain='QQ')
                if p.is_constant() and not p.is_zero:
                    is_proper = False
                    break
                    
        h1_ok = is_nonzero and is_proper
    except Exception:
        h1_ok = False
        
    try:
        # neg_Q: R/I is not Artinian
        # R = QQ[vars]. R/I is Artinian iff I is zero-dimensional.
        if not vars:
            is_artinian = True
        else:
            gb = groebner(gens, *vars, domain='QQ')
            lms = []
            for g in gb:
                p = Poly(g, *vars, domain='QQ')
                if not p.is_zero:
                    lms.append(p.monoms()[0])
            
            if not lms:
                is_artinian = False
            else:
                is_artinian = True
                for i in range(len(vars)):
                    found = False
                    for lm in lms:
                        # Check if lm is a pure power of vars[i]
                        if all(lm[j] == 0 for j in range(len(vars)) if j != i):
                            found = True
                            break
                    if not found:
                        is_artinian = False
                        break
        neg_q_ok = not is_artinian
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a non-zero proper ideal of R",
    "¬Q: R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1