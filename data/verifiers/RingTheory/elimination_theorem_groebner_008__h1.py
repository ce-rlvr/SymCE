import sympy
from sympy import groebner, LM, denom
from sympy.abc import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: G is a Groebner basis of I with respect to the lexicographic order x_1 > x_2 > ... > x_n",
    "H_2: ell is an integer such that 0 <= ell <= n",
    "not Q: G intersect k_elim is not a Groebner basis of the elimination ideal I intersect k_elim with respect to the induced lexicographic order"
]

def is_groebner_basis(G, I, vars):
    try:
        I_sym = [sympy.sympify(poly) for poly in I]
        G_sym = [sympy.sympify(poly) for poly in G]
        
        if not I_sym:
            return all(poly == 0 for poly in G_sym)
        if not G_sym:
            gb_I = groebner(I_sym, *vars, order='lex')
            return all(poly == 0 for poly in gb_I)
            
        gb_I = groebner(I_sym, *vars, order='lex')
        gb_G = groebner(G_sym, *vars, order='lex')
        
        # Check if G and I generate the same ideal
        if list(gb_I) != list(gb_G):
            return False
            
        # Check if the leading monomials of G generate the initial ideal
        for g_poly in gb_I:
            if g_poly == 0: 
                continue
            lm_g = LM(g_poly, *vars, order='lex')
            divisible = False
            for h_poly in G_sym:
                if h_poly == 0: 
                    continue
                lm_h = LM(h_poly, *vars, order='lex')
                q_div = (lm_g / lm_h).cancel()
                if denom(q_div) == 1:
                    divisible = True
                    break
            if not divisible:
                return False
        return True
    except Exception:
        return False

def intersection(F, elim_vars):
    res = []
    for poly in F:
        poly_sym = sympy.sympify(poly)
        if not any(poly_sym.has(v) for v in elim_vars):
            res.append(poly_sym)
    return res

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        I = witness.get("I", [])
        G = witness.get("G", [])
        ell = witness.get("l", 0)
        vars_list = witness.get("vars", [])
        
        if not isinstance(vars_list, (list, tuple)):
            return [False, False, False]
            
        h1 = is_groebner_basis(G, I, vars_list)
        
        n_vars = len(vars_list)
        h2 = isinstance(ell, int) and 0 <= ell <= n_vars
        
        if not h2:
            neg_q = False
        else:
            elim_vars = vars_list[:ell]
            rem_vars = vars_list[ell:]
            
            G_int = intersection(G, elim_vars)
            I_int = intersection(I, elim_vars)
            
            if not rem_vars:
                I_has_nonzero = any(sympy.sympify(c) != 0 for c in I_int)
                G_has_nonzero = any(sympy.sympify(c) != 0 for c in G_int)
                q_val = (I_has_nonzero == G_has_nonzero)
            else:
                q_val = is_groebner_basis(G_int, I_int, rem_vars)
                
            neg_q = not q_val
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]