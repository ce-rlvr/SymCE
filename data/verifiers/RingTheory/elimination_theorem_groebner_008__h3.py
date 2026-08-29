import sympy
from sympy import groebner, reduced, Poly
from sympy.polys.polytools import is_groebner
from sympy.abc import x, y, z, t, u, v, w

CONDITION_LABELS = [
    "H_1: I is an ideal in the polynomial ring",
    "H_2: G is a Groebner basis of I with respect to the lexicographic order",
    "not Q: G intersect the elimination ring is not a Groebner basis of the elimination ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            I_gens = witness.get('I', [])
            G = witness.get('G', [])
            vars = witness.get('vars', [])
            l = witness.get('l', 0)
        else:
            I_gens, G, vars, l = witness
    except Exception:
        return [False, False, False]
        
    # H_1: I is an ideal in the polynomial ring
    try:
        H1 = isinstance(I_gens, (list, tuple)) and isinstance(vars, (list, tuple)) and len(vars) > 0
        if H1:
            I_gens_expr = [p.as_expr() if hasattr(p, 'as_expr') else p for p in I_gens]
            G_expr = [p.as_expr() if hasattr(p, 'as_expr') else p for p in G]
        else:
            I_gens_expr = []
            G_expr = []
    except Exception:
        H1 = False
        I_gens_expr = []
        G_expr = []

    # H_2: G is a Groebner basis of I with respect to the lexicographic order
    try:
        if not H1 or not isinstance(G, (list, tuple)):
            H2 = False
        else:
            G_expr_clean = [p for p in G_expr if p != 0]
            is_gb = is_groebner(G_expr_clean, *vars, order='lex')
            if not is_gb:
                H2 = False
            else:
                gb_I = groebner(I_gens_expr, *vars, order='lex')
                gb_I_clean = [p for p in list(gb_I) if p != 0]
                
                ideal_eq = True
                for p in I_gens_expr:
                    if p == 0: continue
                    rem = reduced(p, G_expr_clean, *vars, order='lex')[1]
                    if rem != 0:
                        ideal_eq = False
                        break
                if ideal_eq:
                    for p in G_expr_clean:
                        rem = reduced(p, gb_I_clean, *vars, order='lex')[1]
                        if rem != 0:
                            ideal_eq = False
                            break
                H2 = ideal_eq
    except Exception:
        H2 = False

    # not Q: G intersect the elimination ring is NOT a Groebner basis of the elimination ideal
    try:
        if not H1:
            neg_Q = False
        else:
            if 0 <= l <= len(vars):
                elim_vars = vars[l:]
            else:
                elim_vars = []
                
            elim_vars_set = set(elim_vars)
            
            G_l = []
            for g in G_expr:
                if g.free_symbols.issubset(elim_vars_set):
                    G_l.append(g)
                    
            gb_I = groebner(I_gens_expr, *vars, order='lex')
            I_l_gens = []
            for g in list(gb_I):
                if g.free_symbols.issubset(elim_vars_set):
                    I_l_gens.append(g)
                    
            G_l_clean = [p for p in G_l if p != 0]
            I_l_gens_clean = [p for p in I_l_gens if p != 0]
            
            if not elim_vars:
                is_gb_elim = (len(I_l_gens_clean) > 0) == (len(G_l_clean) > 0)
            else:
                is_gb_elim = is_groebner(G_l_clean, *elim_vars, order='lex')
                if is_gb_elim:
                    gb_I_l = groebner(I_l_gens_clean, *elim_vars, order='lex') if I_l_gens_clean else []
                    gb_I_l_clean = [p for p in list(gb_I_l) if p != 0]
                    
                    ideal_eq_l = True
                    for p in I_l_gens_clean:
                        rem = reduced(p, G_l_clean, *elim_vars, order='lex')[1]
                        if rem != 0:
                            ideal_eq_l = False
                            break
                    if ideal_eq_l:
                        for p in G_l_clean:
                            rem = reduced(p, gb_I_l_clean, *elim_vars, order='lex')[1]
                            if rem != 0:
                                ideal_eq_l = False
                                break
                    is_gb_elim = ideal_eq_l
                    
            neg_Q = not is_gb_elim
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]