import sympy
from sympy import groebner, Poly
from sympy.abc import a, b, c, d, x, y, z, t, u, v, w

CONDITION_LABELS = ["H_1: K is an algebraically closed field", "H_2: R is a polynomial ring in n variables over K", "¬Q: M is not of the form (x_1 - a_1, ..., x_n - a_n)"]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            V, M = witness
            if not isinstance(M, (list, tuple)):
                return [False, False, False]
        else:
            M = witness
            if not isinstance(M, (list, tuple)):
                return [False, False, False]
            V = list(set().union(*[getattr(sympy.sympify(expr), 'free_symbols', set()) for expr in M]))
            V = sorted(V, key=lambda s: s.name)
            
        M = [sympy.sympify(e) for e in M]
        
        # K is assumed to be an algebraically closed field (e.g., CC) in our evaluation context
        h1 = True
        
        if isinstance(V, (list, tuple)) and len(V) >= 1 and all(isinstance(var, sympy.Symbol) for var in V):
            if all(e.free_symbols.issubset(set(V)) for e in M):
                if all(e.is_polynomial(*V) for e in M):
                    h2 = True
                    
        if h1 and h2:
            if not M:
                is_form = False
            else:
                gb = groebner(M, *V)
                G = gb.polys
                
                is_form = True
                if len(G) != len(V):
                    is_form = False
                else:
                    expected_lms = set()
                    for i in range(len(V)):
                        exp_t = [0]*len(V)
                        exp_t[i] = 1
                        expected_lms.add(tuple(exp_t))
                    
                    lms = set(g.monoms()[0] for g in G)
                    if lms != expected_lms:
                        is_form = False
                    else:
                        for g in G:
                            monoms = g.monoms()
                            for m in monoms[1:]:
                                if any(exp != 0 for exp in m):
                                    is_form = False
                                    break
                            if not is_form:
                                break
            
            neg_q = not is_form
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]